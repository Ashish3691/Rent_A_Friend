# App configuration (e.g., environment variables, MongoDB URI)

import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "mydatabase")
SECRET_KEY = os.getenv("SECRET_KEY", "yoursecretkey")
