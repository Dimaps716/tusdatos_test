import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    ROOT_PATH = ""

    ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS")
    ALLOW_CREDENTIALS = os.getenv("ALLOW_CREDENTIALS")
    ALLOW_METHODS = os.getenv("ALLOW_METHODS")
    ALLOW_HEADERS = os.getenv("ALLOW_HEADERS")
    
    BASE_URL_API = "https://api.funcionjudicial.gob.ec/"