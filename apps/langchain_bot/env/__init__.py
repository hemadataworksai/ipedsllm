#TODO add author, date
#TODO add role of this class and comments
import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
db_url = os.getenv("DB_URL")
redis_url = os.getenv("REDIS_URL")
redis_token = os.getenv("REDIS_TOKEN")
