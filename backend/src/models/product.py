from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Relationship, Column, JSON, ARRAY
from decimal import Decimal

from models.food_entry import FoodEntry

class Product(SQLModel, table=True):
    __tablename__ = "products"

    barcode: str = Field(primary_key=True, max_length=50)
    product_name: str = Field(nullable=False, max_length=255)
    brand: Optional[str] = Field(default=None, max_length=100)

    # Postgres array columns
    categories: Optional[List[str]] = Field(default=None, sa_column=Column(ARRAY(str)))
    allergens: Optional[List[str]] = Field(default=None, sa_column=Column(ARRAY(str)))

    serving_size_g: Optional[Decimal] = Field(default=None)
    serving_size_unit: Optional[str] = Field(default=None, max_length=20)

    # Nutrition
    calories: Optional[Decimal] = None
    protein_g: Optional[Decimal] = None
    carbs_g: Optional[Decimal] = None
    sugar_g: Optional[Decimal] = None
    fiber_g: Optional[Decimal] = None
    fat_g: Optional[Decimal] = None
    saturated_fat_g: Optional[Decimal] = None
    sodium_mg: Optional[Decimal] = None

    # Ingredient & processing data
    ingredients_text: Optional[str] = None
    ingredients_parsed: Optional[List[Dict[str, Any]]] = Field(
        default=None, sa_column=Column(JSON)
    )
    nova_group: Optional[int] = None

    # Metadata
    image_url: Optional[str] = None
    data_source: Optional[str] = Field(default=None, max_length=20)
    last_updated: datetime = Field(default_factory=datetime.now(datetime.UTC))
    created_at: datetime = Field(default_factory=datetime.now(datetime.UTC))

    # Relationships
    food_entries: List["FoodEntry"] = Relationship(back_populates="product")

