from sqlmodel import Session, select
from models.food_entry import FoodEntry
from models.product import Product
from models.user import User
from dtos.food_entry_request import FoodEntryRequest
from dtos.food_entry_response import FoodEntryResponse
from .product_service import ProductService
from decimal import Decimal
from datetime import date, datetime, timezone
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class FoodEntryService:

    def __init__(self, db: Session, product_service: ProductService):
        self.db = db
        self.product_service = product_service

    async def add_product_by_code(
        self, 
        food_entry_request: FoodEntryRequest, 
        user: User,
    ) -> Optional[FoodEntryResponse]:
        """
        Add a food entry by barcode
        
        Args:
            food_entry_request: Request containing product, serving size, meal type, and notes
            user: The user creating the entry
            
        Returns:
            FoodEntryResponse with calculated nutrition data
        """
        try:
            # Get or fetch product by barcode
            curr_product = await self.product_service.get_product_by_barcode(
                food_entry_request.product.barcode
            )
            
            if not curr_product:
                logger.warning(f"Product not found: {food_entry_request.product.barcode}")
                return None
            
            # Calculate nutrition based on serving size
            serving_size_g = Decimal(str(food_entry_request.serving_size_g))
            multiplier = serving_size_g / Decimal("100.0")
            
            # Calculate nutrition values
            calories = None
            protein_g = None
            carbs_g = None
            sugar_g = None
            fiber_g = None
            fat_g = None
            
            if curr_product.kcalories_100g:
                calories = (curr_product.kcalories_100g * multiplier).quantize(Decimal("0.01"))
            if curr_product.protein_100g:
                protein_g = (curr_product.protein_100g * multiplier).quantize(Decimal("0.01"))
            if curr_product.carbs_100g:
                carbs_g = (curr_product.carbs_100g * multiplier).quantize(Decimal("0.01"))
            if curr_product.sugar_100g:
                sugar_g = (curr_product.sugar_100g * multiplier).quantize(Decimal("0.01"))
            if curr_product.fiber_100g:
                fiber_g = (curr_product.fiber_100g * multiplier).quantize(Decimal("0.01"))
            if curr_product.fat_100g:
                fat_g = (curr_product.fat_100g * multiplier).quantize(Decimal("0.01"))
            
            food_entry = FoodEntry(
                user_id=user.id,
                barcode=curr_product.barcode,
                meal_type=food_entry_request.meal_type,
                servings=serving_size_g,
                calories=calories,
                protein_g=protein_g,
                carbs_g=carbs_g,
                sugar_g=sugar_g,
                fiber_g=fiber_g,
                fat_g=fat_g,
                custom_food_name=None,
                notes=food_entry_request.notes,
                created_at=datetime.now(timezone.utc)
            )
            
            # Save to database
            self.db.add(food_entry)
            self.db.commit()
            self.db.refresh(food_entry)
            
            logger.info(f"Food entry created: {food_entry.id} for user {user.id}")
            
            # Return response
            return FoodEntryResponse(
                id=food_entry.id,
                user_id=food_entry.user_id,
                barcode=food_entry.barcode,
                entry_date=food_entry.entry_date,
                timezone=food_entry.timezone,
                meal_type=food_entry.meal_type,
                servings=food_entry.servings,
                calories=food_entry.calories,
                protein_g=food_entry.protein_g,
                carbs_g=food_entry.carbs_g,
                sugar_g=food_entry.sugar_g,
                fiber_g=food_entry.fiber_g,
                fat_g=food_entry.fat_g,
                custom_food_name=food_entry.custom_food_name,
                notes=food_entry.notes,
                created_at=food_entry.created_at
            )
            
        except Exception as e:
            logger.error(f"Error creating food entry: {str(e)}")
            self.db.rollback()
            return None

    async def delete_product_by_code(
        self,
        food_entry_id: int,
        user: User
    ) -> bool:
        try:
            statement = select(FoodEntry).where(
                FoodEntry.id == food_entry_id,
                FoodEntry.user_id == user.id
            )
            food_entry = self.db.exec(statement).first()
            
            if not food_entry:
                logger.warning(f"Food entry not found: {food_entry_id} for user {user.id}")
                return False
            
            # Delete the food entry
            self.db.delete(food_entry)
            self.db.commit()
            
            logger.info(f"Food entry deleted: {food_entry_id} for user {user.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting food entry: {str(e)}")
            self.db.rollback()
            return False