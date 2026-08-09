import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
  MODEL_NAME: str = "mistral-medium"
  TEMPERATURE: float = float(os.getenv("MISTRAL_TEMPERATURE", "0.2"))
  API_KEY: str = os.getenv("MISTRAL_API_KEY", "")

  @classmethod
  def validate(cls):
    if not cls.API_KEY:
      raise ValueError("MISTRAL_API_KEY is missing from environment variables.")
