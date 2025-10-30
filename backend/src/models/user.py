from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from models.food_entry import FoodEntry

# ---------------------------
# Users Table
# ---------------------------
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(primary_key=True, max_length=128)  # Firebase UID
    email: str = Field(unique=True, index=True, nullable=False, max_length=255)
    display_name: Optional[str] = Field(default=None, max_length=100)
    created_at: datetime = Field(default_factory=datetime.now(datetime.UTC))
    updated_at: datetime = Field(default_factory=datetime.now(datetime.UTC))

    # Relationships
    food_entries: List["FoodEntry"] = Relationship(back_populates="user")
