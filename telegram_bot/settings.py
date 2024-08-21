import os

from dotenv import load_dotenv, find_dotenv

# api_url = 'http://45.128.207.173:8070/api'
api_url = 'http://5.253.62.213:8070/api'

load_dotenv(find_dotenv())
token = os.getenv("token")

headers = {"Authorization": f"Bearer test"}

# BOT_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOT_BASE_DIR = os.getcwd()
