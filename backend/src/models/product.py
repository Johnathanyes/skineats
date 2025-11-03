from datetime import datetime, timezone
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Index, Column as SAColumn, Text
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

    # Nutrition
    kcalories_100g: Optional[Decimal] = None
    protein_100g: Optional[Decimal] = None
    carbs_100g: Optional[Decimal] = None
    sugar_100g: Optional[Decimal] = None
    fiber_100g: Optional[Decimal] = None
    fat_100g: Optional[Decimal] = None
    saturated_fat_100g: Optional[Decimal] = None
    sodium_100g: Optional[Decimal] = None

    skin_score: Optional[int] = None
    skin_score_breakdown: Optional[List[Dict[str, Any]]] = Field(
        default=None, sa_column=SAColumn(JSONB)
    )

    # Ingredient & processing data
    ingredient_list: Optional[List[Dict[str, str]]] = Field(
        default=None, sa_column=SAColumn(JSONB)
    )
    nova_group: Optional[int] = None
    ecoscore: Optional[str]
    allergen_tags: Optional[List[str]] = Field(
        default=None, sa_column=SAColumn(PG_ARRAY(Text()))
    )
    labels_tag: Optional[List[str]]

    # Metadata
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    # Relationships
    food_entries: List["FoodEntry"] = Relationship(back_populates="product")
    favorites: List["UserFavorite"] = Relationship(back_populates="product")

    # Indexes per schema
    __table_args__ = (
        Index("idx_products_name", "product_name"),
        Index("idx_products_brand", "brand"),
    )

