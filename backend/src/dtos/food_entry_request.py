from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel
from models.product import Product


class FoodEntryRequest(SQLModel):
    product: Product
    serving_size_g: float
    meal_type: Optional[str]
    notes: Optional[str]