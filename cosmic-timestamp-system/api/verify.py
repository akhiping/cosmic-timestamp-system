import json
from src.timestamp_system import verify_seal

def handler(request):
    body = json.loads(request["body"])
    result = verify_seal(body["text"], body["seal"])

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
    }
