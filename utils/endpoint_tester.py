import requests
import json

port = 8080
base_url = f"http://localhost:{port}/v1"


def check_health():
    print("Testing health...")
    url = f"{base_url}/health/"
    res = requests.get(url)
    return res.json()


def check_notify():
    print("Testing notify...")
    url = f"{base_url}/notify/"
    data = {"topic": "pricing", "description": "Help with sales inquiry"}
    res = requests.post(url, json=data)
    response_json = res.json()
    return response_json


if __name__ == "__main__":
    response = check_health()
    status = response["status"]
    print(f"Health check: {status}")

    response = check_notify()
    print(f"Notify Response: {response}")
