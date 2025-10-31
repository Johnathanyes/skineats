import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

if not os.getenv("VERCEL"):
    # You can control which .env file to load locally
    env_file = ".env.development"
    load_dotenv(env_file)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

# Ensure async driver (asyncpg) regardless of provided scheme
def _to_async_url(url: str) -> str:
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if url.startswith("postgresql://") and "+asyncpg" not in url:
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url

ASYNC_DATABASE_URL = _to_async_url(DATABASE_URL)
IS_VERCEL = bool(os.getenv("VERCEL"))

engine_kwargs = {
    "echo": False,
    "future": True,
    "pool_pre_ping": True,
}

if IS_VERCEL:
    # NullPool doesn't accept pool_size/max_overflow
    engine_kwargs["poolclass"] = NullPool
else:
    engine_kwargs["pool_size"] = 1
    engine_kwargs["max_overflow"] = 0

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    **engine_kwargs,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session