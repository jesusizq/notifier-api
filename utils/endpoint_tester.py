import requests

def test_app():
    print("Testing app...")
    url = "http://localhost:5000/v1/tasks/health"
    res = requests.get(url)
    return res.json()


if __name__ == "__main__":
    response = test_app()
    status = response["status"]
    print(f"Status {status}")
