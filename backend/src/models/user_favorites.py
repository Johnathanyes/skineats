from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint, CheckConstraint, Index, Column as SAColumn, ForeignKey, String

if TYPE_CHECKING:
    from models.product import Product
    from models.user import User

class UserFavorite(SQLModel, table=True):
    __tablename__ = "user_favorites"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(
        sa_column=SAColumn(String(128), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    )
    barcode: str = Field(
        default=None,
        sa_column=SAColumn(String(50), ForeignKey("products.barcode"), nullable=False),
    )
    custom_food_name: Optional[str] = Field(default=None, max_length=255)

    usage_count: int = Field(default=0)

    last_used: datetime = Field(default_factory=datetime.now(datetime.UTC))
    created_at: datetime = Field(default_factory=datetime.now(datetime.UTC))

    user: "User" = Relationship(back_populates="user_favorites")
    product: Optional["Product"] = Relationship(back_populates="favorites")

    __table_args__ = (
        UniqueConstraint("user_id", "barcode", name="uq_user_favorites_user_barcode"),
        Index("idx_favorites_user", "user_id", "usage_count"),
    )