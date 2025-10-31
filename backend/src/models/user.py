from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.food_entry import FoodEntry
    from models.user_favorites import UserFavorite

# ---------------------------
# Users Table
# ---------------------------
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(primary_key=True, max_length=128)  # Firebase UID
    email: str = Field(unique=True, index=True, nullable=False, max_length=255)
    display_name: Optional[str] = Field(default=None, max_length=100)
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    # Relationships
    food_entries: List["FoodEntry"] = Relationship(back_populates="user")
    user_favorites: List["UserFavorite"] = Relationship(back_populates="user")
