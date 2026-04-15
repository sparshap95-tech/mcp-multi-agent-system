import json
import requests

payload = {
    "jsonrpc": "2.0",
    "method": "add",
    "params": [3, 5],
    "id": 1
}

response = requests.post(
    "http://localhost:4000",
    json=payload
)

print("Raw response:", response.text)
print("Parsed result:", response.json()["result"])