import json
from src.timestamp_system import seal_document

def handler(request):
    body = json.loads(request["body"])
    text = body["text"]
    frb_name = body["frb_name"]

    result = seal_document(text, frb_name)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
    }
