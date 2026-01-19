import json
from src.timestamp_system import load_frbs

def handler(request):
    frbs = load_frbs()
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(frbs)
    }
