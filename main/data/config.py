from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("TOKEN")
chat_id = os.getenv("CHAT_ID")