import requests
import json


def check_health():
    print("Testing health...")
    url = "http://localhost:5000/v1/health"
    res = requests.get(url)
    return res.json()


def check_notify():
    print("Testing notify...")
    url = "http://localhost:5000/v1/notify/"
    data = {"topic": "sales", "description": "Help with sales inquiry"}
    res = requests.post(url, json=data)
    response_json = res.json()
    print(f"Notify Response: {response_json}")
    return response_json


if __name__ == "__main__":
    response = check_health()
    status = response["status"]
    print(f"Status {status}")

    response = check_notify()
