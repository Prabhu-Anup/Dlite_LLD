import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class to hold database credentials.
    These are loaded from the .env file.
    """
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')

class Messages:
    """
    Messages class to hold all user-facing strings.
    These are loaded from the .env file for easy customization.
    """
    WELCOME = os.getenv('MSG_WELCOME')
    MENU = os.getenv('MSG_MENU')
    PROMPT_ADDED = os.getenv('MSG_PROMPT_ADDED')
    PROMPT_NOT_FOUND = os.getenv('MSG_PROMPT_NOT_FOUND')
    PROMPT_UPDATED = os.getenv('MSG_PROMPT_UPDATED')
    PROMPT_DELETED = os.getenv('MSG_PROMPT_DELETED')
    NO_PROMPTS = os.getenv('MSG_NO_PROMPTS')
    SEARCH_PROMPT = os.getenv('MSG_SEARCH_PROMPT')
    FAVORITE_TOGGLED = os.getenv('MSG_FAVORITE_TOGGLED')
    INVALID_CHOICE = os.getenv('MSG_INVALID_CHOICE')
    EXIT = os.getenv('MSG_EXIT')
