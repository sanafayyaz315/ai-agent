from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(), override=True)

API_KEY = os.environ.get("API_KEY")
MODEL = os.environ.get("MODEL")

