# OverTheWire: Natas Level 5 -> Level 6 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to retrieve the password for Natas Level 6. Upon accessing the page, the server returns an **"Access disallowed"** state accompanied by the error message: `"You are not logged in"`. 

Inspecting the HTML source code reveals no clues, hidden credentials, or comments. In web applications, login states and user sessions are typically maintained via client-side tokens. This prompt indicates that the application relies on an insecure client-side session flag, presenting an **Insecure Session Management** vulnerability.

## 2. Solution Strategy & Exploitation
Since HTTP is a stateless protocol, websites use cookies stored in the user's browser to remember identity states. If the application handles authentication solely by checking a basic Boolean flag inside a cookie without backend cryptographic verification, an attacker can manipulate this value to escalate privileges.

### Step-by-step Execution:
1. Access the challenge page.
2. Open the browser's **Developer Tools (F12)** and navigate to the **Application** (or Storage/Network) tab.
3. Locate the **Cookies** section for the current domain.
4. Inspect the defined cookies and discover a suspicious pair:
   * **Name**: `loggedin`
   * **Value**: `0`
5. Double-click the value and alter it from `0` (False/Not logged in) to `1` (True/Logged in).
6. Refresh the page to resend the request with the modified cookie payload.

### Result Analysis:
The backend validates the tampered cookie blindly, successfully grants session access, and outputs the flag:
```text
Access granted. The password for natas6 is 7mhjtShJAcld2NYbKHEadnhEwRn2P8VT
```

## 3. Flag / Final Result
* **Natas Level 6 Password**: `7mhjtShJAcld2NYbKHEadnhEwRn2P8VT`
