from datetime import datetime
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Index, Column as SAColumn, String, Integer, Numeric, Text
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY, JSONB

if TYPE_CHECKING:
    from models.food_entry import FoodEntry
    from models.user_favorites import UserFavorite

class Product(SQLModel, table=True):
    __tablename__ = "products"

    barcode: str = Field(primary_key=True, max_length=50)
    product_name: str = Field(nullable=False, max_length=255)
    brand: Optional[str] = Field(default=None, max_length=100)

    # Postgres array columns
    categories: Optional[List[str]] = Field(
        default=None, sa_column=SAColumn(PG_ARRAY(Text()))
    )

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

    skin_score: Optional[int] = None
    skin_score_breakdown: Optional[List[Dict[str, Any]]] = Field(
        default=None, sa_column=SAColumn(JSONB)
    )

    # Ingredient & processing data
    ingredients_text: Optional[str] = None
    ingredients_parsed: Optional[List[Dict[str, Any]]] = Field(
        default=None, sa_column=SAColumn(JSONB)
    )
    nova_group: Optional[int] = None
    allergens: Optional[List[str]] = Field(
        default=None, sa_column=SAColumn(PG_ARRAY(Text()))
    )

    # Metadata
    image_url: Optional[str] = None
    data_source: Optional[str] = Field(default=None, max_length=20)
    created_at: datetime = Field(default_factory=datetime.now(datetime.UTC))
    updated_at: datetime = Field(default_factory=datetime.now(datetime.UTC))

    # Relationships
    food_entries: List["FoodEntry"] = Relationship(back_populates="product")
    favorites: List["UserFavorite"] = Relationship(back_populates="product")

    # Indexes per schema
    __table_args__ = (
        Index("idx_products_name", "product_name"),
        Index("idx_products_brand", "brand"),
    )

