from datetime import datetime, date, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal
from sqlalchemy import Index, Column as SAColumn, ForeignKey, String

if TYPE_CHECKING:
    from models.product import Product
    from models.user import User

# ---------------------------
# Food Diary Entries
# ---------------------------
class FoodEntry(SQLModel, table=True):
    __tablename__ = "food_entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(
        sa_column=SAColumn(String(128), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    )
    barcode: str = Field(
        default=None,
        sa_column=SAColumn(String(50), ForeignKey("products.barcode"), nullable=False),
    )

    entry_date: date = Field(nullable=False)
    timezone: str = Field(default="UTC", max_length=50)
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
    notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now(timezone.UTC))

    # Relationships
    user: "User" = Relationship(back_populates="food_entries")
    product: Optional["Product"] = Relationship(back_populates="food_entries")

    __table_args__ = (
        Index("idx_food_entries_user_date", "user_id", "entry_date", postgresql_using=None, postgresql_ops=None),
        Index("idx_food_entries_user_created", "user_id", "created_at"),
    )
