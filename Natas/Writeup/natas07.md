# OverTheWire: Natas Level 7 -> Level 8 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to retrieve the password for Natas Level 8. Upon inspecting the page source code, a direct hint is provided regarding the absolute path of the next level's password file:
```html
<!-- hint: password for webuser natas8 is in /etc/natas_webpass/natas8 -->
```
When interacting with the navigation links ("Home" and "About"), the URL structural behavior changes to use a query parameter:
```text
http://natas7.natas.labs.overthewire.org/index.php?page=home
```
This design indicates that the backend dynamically handles page routing by passing the parameter value directly into a file inclusion function (such as `include()` or `require()`) in PHP. Because there is no input validation or whitelisting on this parameter, the application suffers from a critical **Local File Inclusion (LFI)** vulnerability.

## 2. Solution Strategy & Exploitation
An LFI vulnerability allows an attacker to manipulate the file path parameter to read arbitrary files hosted on the server filesystem, provided the web server process has adequate read permissions. We can leverage the absolute path provided in the source comment to force the server to include and display the password file.

### Step-by-step Execution:
1. Access the challenge page and identify the target file location from the source comment: `/etc/natas_webpass/natas8`.
2. Identify the vulnerable parameter controlling file routing: `page`.
3. Inject the absolute file path directly into the `page` parameter by modifying the URL in the browser address bar to:
   ```text
   http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8
   ```
4. Execute the request. The backend processes the input, reads the specified system file, and renders its raw contents directly onto the web page.

### Result Analysis:
The server includes the targeted credential file successfully and outputs the cleartext password flag:
```text
ugXL95KQmUAJJj6bMezOlBNDyI9Imwkc
```

## 3. Flag / Final Result
* **Natas Level 8 Password**: `ugXL95KQmUAJJj6bMezOlBNDyI9Imwkc`
