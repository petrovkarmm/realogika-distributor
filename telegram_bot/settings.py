import os

# api_url = 'http://45.128.207.173:8070/api'
api_url = 'https://5.253.62.213:8070/api'

token = os.getenv("BOT_TOKEN")

headers = {"Authorization": f"Bearer {token}"}

# BOT_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOT_BASE_DIR = os.getcwd()
