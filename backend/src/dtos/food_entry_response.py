from sqlmodel import SQLModel
from typing import Optional
from decimal import Decimal
from datetime import date, datetime

class FoodEntryResponse(SQLModel):
    id: Optional[int]
    user_id: str
    barcode: str
    
    meal_type: Optional[str]
    servings: Decimal
    
    calories: Optional[Decimal]
    protein_g: Optional[Decimal]
    carbs_g: Optional[Decimal]
    sugar_g: Optional[Decimal]
    fiber_g: Optional[Decimal]
    fat_g: Optional[Decimal]
    
    custom_food_name: Optional[str]
    notes: Optional[str]
    created_at: datetime


