# OverTheWire: Natas Level 2 -> Level 3 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to find the password for Natas Level 3. Upon inspecting the main page, there are no visible credentials hidden in the HTML comments. However, securing a web application requires not only secure code but also secure server configurations. 

This level tests the ability to identify exposed sensitive directories and files, a flaw known as **Insecure Directory Listing** or **Information Disclosure**.

## 2. Solution Strategy & Exploitation
By analyzing the source code, we can look for asset paths (like images, CSS, or JS) to see how the server structures its public files, and check if those directories allow unauthorized browsing.

### Step-by-step Execution:
1. Access the challenge page, **right-click**, and select **"View page source"**.
2. Scan the HTML and locate a suspicious image tag referencing an external directory:
   ```html
   <img src="files/pixel.png">
   ```
3. Navigate directly to the parent directory by modifying the URL in the browser address bar to:
   ```text
   http://natas2.natas.labs.overthewire.org/files/
   ```
4. Due to misconfigured directory listing permissions on the server, the browser displays an index of the `/files/` directory.
5. Among the files, a suspicious text file named `users.txt` is discovered.
6. Open `users.txt` to find a list of credentials, which contains the cleartext password for the next level:
   ```text
   natas3:K30JrSRHzjxq3paUQuwozY4MNvmNFyhI
   ```

## 3. Flag / Final Result
* **Natas Level 3 Password**: `K30JrSRHzjxq3paUQuwozY4MNvmNFyhI`
