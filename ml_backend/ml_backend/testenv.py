from dotenv import load_dotenv
import os

load_dotenv()

print("KEY:", os.environ.get("GROQ_API_KEY"))