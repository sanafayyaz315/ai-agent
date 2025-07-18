from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv(), override=True)

API_KEY = os.environ.get("API_KEY")
MODEL = os.environ.get("MODEL")

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))

CHAINLIT_DB_NAME = os.environ.get("CHAINLIT_DB_NAME")
CHAINLIT_DB_USER = os.environ.get("CHAINLIT_DB_USER")
CHAINLIT_DB_PASSWORD = os.environ.get("CHAINLIT_DB_PASSWORD")
CHAINLIT_DB_HOST = os.environ.get("CHAINLIT_DB_HOST")
CHAINLIT_DB_PORT = os.environ.get("CHAINLIT_DB_PORT")

MAX_ITERATIONS = int(os.environ.get("MAX_ITERATIONS"))

SCHEMA_PATH = os.environ.get("SCHEMA_PATH")

with open("../templates/calculator.txt", "r") as f:
    SYSTEM_PROMPT_TEMPLATE_CALCULATOR = f.read()

with open("../templates/sql_agent_json.txt", "r") as f:
    SYSTEM_PROMPT_TEMPLATE_SQL = f.read()

with open("../database/scripts/schema.sql", "r") as f:
    DB_SCHEMA = f.read()

