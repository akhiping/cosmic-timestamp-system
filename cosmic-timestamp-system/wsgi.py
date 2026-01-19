"""
WSGI entry point for production deployment (Gunicorn/Render)
"""
import sys
import os
import importlib.util

# Load the Flask app from the numbered Python file
spec = importlib.util.spec_from_file_location(
    "web_demo", 
    os.path.join(os.path.dirname(__file__), "src", "04_build_web_demo.py")
)
web_demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(web_demo)

# Export the Flask app for Gunicorn
app = web_demo.app

