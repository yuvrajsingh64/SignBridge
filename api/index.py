import sys
import os

# Point explicitly to the project root directory
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app

# Export for Vercel WSGI
handler = app
app = app
