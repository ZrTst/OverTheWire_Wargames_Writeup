# OverTheWire: Natas Level 22 -> Level 23 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to bypass an enforced page redirection mechanism and read a privileged secret value containing the password for Natas Level 23.

Upon accessing the endpoint, providing the query trigger variable `?revelio=1` causes the browser to instantly bounce back to the main `index.php` login home. Inspecting the challenge backend source code exposes a catastrophic flaw in the application's execution flow logic:

```php
if(array_key_exists("revelio", $_GET)) {

    // only admins can reveal the password
    if(!($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1)) {
    header("Location: /");
    }
}
?>
```

### The Core Vulnerability: Execution Flow Control Flaw via Missing Termination
The vulnerability is rooted in a fundamental misunderstanding of how HTTP redirection behaviors interact with server-side execution runtime environments:
* **The Mechanics of `header("Location: ...")`**: Invoking this routine in PHP instructs the web server to append an `HTTP 302 Found` header response back to the client [🔍](https://php.net). 
* **The Non-Blocking Nature**: Emitting a 302 header directive is a **non-blocking action**. It does *not* inherently terminate the execution thread of the active PHP engine script. Because the developer neglected to couple the redirection with a explicit termination construct (such as `exit;` or `die();`), the script seamlessly continues executing line-by-line in the background.
* **The Client-Side Illusion**: The server successfully invokes `showsecret()`, attaches the raw password credentials to the response payload, and transmits the complete packet down to the browser. However, standard browsers (like Chrome) are programmed to automatically parse the `302` response header and immediately pull the user away to the new location before rendering the intercepted response block body.

---

## 2. Solution Strategy & Exploitation

### The Security Axiom: Front-End Obfuscation vs. Back-End Exposure
This vulnerability validates a foundational principle of offensive security: **Never trust client-side controls.** Once sensitive data leaves the boundary of the server infrastructure and enters the network transport pipe, the client exercises absolute ownership over how that data is indexed, processed, or viewed.

Standard browsers automatically drop or blind-redirect HTTP responses featuring 302 codes, outputting errors like `Failed to load response data`. To extract the hidden flag payload, an attacker simply needs to instruct the client-side tooling to ignore the redirect notification and capture the raw stream buffers directly.

### Method 1: Bypassing Redirects via Command-Line cURL (Recommended)
Command-line utilities such as `curl` are inherently stateless and completely immune to structural location tracking unless the explicitly verbose redirection flag (`-L`) is manually supplied. By dispatching a naked raw query request, the server faithfully drops the flag output straight into the standard console terminal log screen.

Open your local Command Prompt (`cmd`) or terminal shell environment, and dispatch the target script query:
```bash
curl -u natas22:964laB0r7TuDqJj5b3HFtwsQoc0GhjBF "http://natas22.natas.labs.overthewire.org?revelio=1"
```

### Analysis of the Terminal Output Stream:
Upon firing, the command line interface bypasses the 302 instruction entirely, capturing the hidden text chunk trailing right below the header:

```text
You are an admin. The credentials for the next level are:<br><pre>Username: natas23
Password: CH1OBxJy8uAxMM15Nx6VXSMwcJbBbnS5</pre>
```

---

## 3. Flag / Final Result
* **Natas Level 23 Password**: `CH1OBxJy8uAxMM15Nx6VXSMwcJbBbnS5`
