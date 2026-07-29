# OverTheWire: Natas Level 12 -> Level 13 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to retrieve the password for Natas Level 13. The web page provides a file upload feature, seemingly designed to accept images. 

By analyzing the frontend code and the upload form structure, we can check how the application determines the uploaded file's destination name and extension. If the server trusts client-side parameters to define file types, it introduces a severe **Arbitrary File Upload** vulnerability, potentially leading to Remote Code Execution (RCE).

## 2. Solution Strategy & Exploitation
We can construct a malicious PHP script (often referred to as a WebShell or Trojan Horse) to execute system commands on the server. If we can force the application to store and execute this script with a `.php` extension rather than an image extension, the web server's PHP interpreter will parse our code.

### WebShell Payload Construction:
We create a simple script to print the contents of the password store:
```php
<?php
system('cat /etc/natas_webpass/natas13');
?>
```

### Step-by-step Execution:
1. Access the challenge upload page.
2. Open the browser's **Developer Tools (F12)** and inspect the form elements.
3. Locate a highly vulnerable hidden input tag responsible for setting the uploaded file's extension:
   ```html
   <input type="hidden" name="filename" value="[random_string].jpg" />
   ```
4. Double-click the `value` attribute and modify it to use a `.php` extension (e.g., `payload.php`).
5. Browse and select the constructed PHP malicious file, then click the **Upload** button.
6. The server accepts the request and blindly uses our modified extension to save the file.
7. Click the link provided by the interface to navigate directly to the uploaded file's path.

### Result Analysis:
The server routes the request to our `.php` file, triggers the underlying `system()` wrapper, reads the system's sensitive credential database, and returns the cleartext flag:
```text
g8ba0olAzaSJuyS4gnmbdVVigAICLG1k
```

## 3. Flag / Final Result
* **Natas Level 13 Password**: `g8ba0olAzaSJuyS4gnmbdVVigAICLG1k`
