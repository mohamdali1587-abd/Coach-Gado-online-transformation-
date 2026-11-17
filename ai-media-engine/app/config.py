import os
from dotenv import load_dotenv
load_dotenv()
def get(name, default=""): return os.getenv(name, default)
def enabled(name): return get(name, "false").lower() in ("1","true","yes","on")
