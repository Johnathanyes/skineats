import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Manages application settings, loading from a .env file or environment variables.
    """
    
    environment_type: str = os.getenv("ENVIRONMENT_TYPE", "development")
    
    # --- For Development (reading from .env file) ---
    open_food_facts_api_url: str

    # --- For Production (Vercel) ---
    # These will be read from Vercel's environment variables
    firebase_project_id: str
    firebase_client_email: str
    firebase_private_key: str
    
    # Model config to load from a .env file for local dev
    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('ENVIRONMENT_TYPE', 'development')}", 
        env_file_encoding='utf-8',
        extra='ignore'
    )

# Create a single, importable instance of the settings
settings = Settings()
    