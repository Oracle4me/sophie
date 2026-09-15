import os

from dotenv import load_dotenv


load_dotenv("config/.env")


class Settings:
    app_name: str = os.getenv("SOPHIE_NAME", "Sophie")
    environment: str = os.getenv("SOPHIE_ENV", "development")

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    llm_model: str = os.getenv("SOPHIE_LLM_MODEL", "gpt-5.6-luna")


settings = Settings()