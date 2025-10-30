from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal

from models.product import Product
from models.user import User

# ---------------------------
# Food Diary Entries
# ---------------------------
class FoodEntry(SQLModel, table=True):
    __tablename__ = "food_entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", nullable=False)
    barcode: Optional[str] = Field(foreign_key="products.barcode", default=None)

    entry_date: date = Field(nullable=False)
    meal_type: Optional[str] = Field(default=None, max_length=20)
    servings: Decimal = Field(default=Decimal("1.0"))

    # Snapshot nutrition
    calories: Optional[Decimal] = None
    protein_g: Optional[Decimal] = None
    carbs_g: Optional[Decimal] = None
    sugar_g: Optional[Decimal] = None
    fiber_g: Optional[Decimal] = None
    fat_g: Optional[Decimal] = None

    custom_food_name: Optional[str] = Field(default=None, max_length=255)
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional[User] = Relationship(back_populates="food_entries")
    product: Optional[Product] = Relationship(back_populates="food_entries")
