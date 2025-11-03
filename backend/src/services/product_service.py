from sqlmodel import Session, select
from models.product import Product, ProductResponse
from .clients.open_food_facts_client import OpenFoodFactsClient
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class ProductService:
    
    def __init__(self, db: Session):
        self.db = db
        self.off_client = OpenFoodFactsClient()
    
    async def close(self):
        """Close external clients"""
        await self.off_client.close()
    
    async def get_product_by_barcode(self, barcode: str) -> Optional[Product]:

        statement = select(Product).where(Product.barcode == barcode)
        product = self.db.exec(statement).first()
        
        if product:
            logger.info(f"Product found in database: {barcode}")
            return product
        
        # 2. Product not in DB - fetch from OpenFoodFacts
        logger.info(f"Fetching product from OpenFoodFacts: {barcode}")
        product_data = await self.off_client.get_product(barcode)
        
        if not product_data:
            logger.warning(f"Product not found in OpenFoodFacts: {barcode}")
            return None
        
        # 3. Save product to database
        product = Product(**product_data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        
        logger.info(f"Product saved to database: {barcode}")
        return product
    
    def search_products(
        self, 
        query: str, 
        limit: int = 20, 
        offset: int = 0
    ) -> list[Product]:
        """
        Search products by name or brand
        
        Args:
            query: Search query
            limit: Maximum results to return
            offset: Pagination offset
            
        Returns:
            List of matching products
        """
        statement = (
            select(Product)
            .where(
                (Product.name.ilike(f"%{query}%")) | 
                (Product.brand.ilike(f"%{query}%"))
            )
            .offset(offset)
            .limit(limit)
        )
        
        products = self.db.exec(statement).all()
        return list(products)