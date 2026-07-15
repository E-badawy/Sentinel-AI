from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    APP_NAME: str = "Sentinel AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Search
    TAVILY_API_KEY: str = ""
    
    # AI
    LLM_PROVIDER: str = "groq"

    LLM_API_KEY: str = ""

    LLM_BASE_URL: str = "https://api.groq.com/openai/v1"

    LLM_MODEL: str = "llama-3.3-70b-versatile"
    GEMINI_API_KEY: str = ""
    GEMINI_TEXT_MODEL: str = "models/gemini-2.5-flash"
    GEMINI_VISION_MODEL: str = "models/gemini-3.1-flash-image"
    
       
    # WhatsApp
    WHATSAPP_ACCESS_TOKEN: str = ""
    WHATSAPP_PHONE_NUMBER_ID: str = ""
    WHATSAPP_VERIFY_TOKEN: str = ""
    META_APP_SECRET: str = ""
    
    # Email
    EMAIL_ADDRESS: str = ""
    EMAIL_APP_PASSWORD: str = ""
    EMAIL_SMTP_SERVER: str = "smtp.gmail.com"
    EMAIL_SMTP_PORT: int = 587

    MEDIA_FOLDER: str = "app/media/images"
      
    ALLOWED_USERS: str = Field(default="")
    @property
    def allowed_users(self):

         return [
        user.strip()
        for user in self.ALLOWED_USERS.split(",")
        if user.strip()
        ]
    
    DATABASE_URL: str = ""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

