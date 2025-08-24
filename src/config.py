import os
from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN=os.getenv("BOT_TOKEN")

USER_DB=os.getenv("USER_DB")
PASSWORD_DB=os.getenv("PASSWORD_DB")
NAME_DB=os.getenv("NAME_DB")
HOST_DB=os.getenv("HOST_DB")
PORT_DB=os.getenv("PORT_DB")

CHAT_ID=os.getenv("CHAT_ID")

ADMIN=os.getenv("ADMIN")

USERS_PER_PAGE = 5
APPLICATIONS_PER_PAGE = 5
