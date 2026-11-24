# Central configuration for the Agentic Research Assistant

import os
from pathlib import Path
from dotenv import load_dotenv

# Locate the .env file in the project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# API credentials
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
NCBI_EMAIL = os.getenv("NCBI_EMAIL")

# Language model settings
MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0