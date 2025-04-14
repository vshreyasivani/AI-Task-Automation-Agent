import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = "gpt-3.5-turbo"  # Free tier has access to 3.5
    
    # Fallback configuration
    USE_OLLAMA = False
    OLLAMA_MODEL = "llama3"  # If using local Ollama
    
    # Agent behavior
    MAX_RETRIES = 3
    SAFE_MODE = True  # Always ask for confirmation before executing