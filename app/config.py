import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    def __init__(self):
        # Core settings with safe defaults
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "fallback-key")
        self.serpapi_key = os.getenv("SERPAPI_KEY", "not-configured")
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # CORS settings
        self.cors_origins = [
            "https://spectacular-dusk-cc7b08.netlify.app", 
            "http://localhost:3000",
            "*"
        ]

# Create global settings instance
settings = Settings()