from datetime import datetime
from fastapi import APIRouter, Depends
from sqlmodel import select
from auth.auth import get_current_user
from models.user import User
from db.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post("/sync")
async def sync_user(
    decoded_token: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Sync a Firebase-authenticated user into the local SQLAlchemy database.
    If user already exists, update their updated_at timestamp.
    """
    uid = decoded_token.get("uid")
    user_email = decoded_token.get("email")
    user_display_name = decoded_token.get("name")

    result = await db.execute(select(User).where(User.id == uid))
    user = result.scalar_one_or_none()
    if not user:
        new_user = User(
            id=uid,
            email=user_email,
            display_name=user_display_name,
            created_at=datetime.now(datetime.UTC),
            updated_at=datetime.now(datetime.UTC),
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return {
            "status": "created",
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "display_name": new_user.display_name,
            },
        }
    user.updated_at = datetime.now(datetime.UTC)
    db.add(user)
    await db.commit()
    return {
        "status": "exists",
        "user": {
            "id": user.id,
            "email": user.email,
            "display_name": user.display_name,
        },
    }

    