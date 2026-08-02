# OverTheWire: Natas Level 20 -> Level 21 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to compromise the session mechanism, escalate privileges to an administrative role, and retrieve the password for Natas Level 21. Unlike previous levels that suffered from weak session identifiers, this level shifts toward custom session storage implementation.

The application relies on `session_set_save_handler()` to override standard PHP session serialization. The backend utilizes two critical custom functions for data persistence:
* **Serialization (`mywrite`)**: Iterates through the `$_SESSION` superglobal array and writes data to a local server text file format using key-value parsing separated by a space and delimited by a newline character (`$data .= "$key $value\n"`).
* **Deserialization (`myread`)**: Reads the session file line-by-line via `fgets()` or `file()`, stripping trailing newlines and splitting the string at the *first occurrence* of a space character to rebuild key-value assignments (`$_SESSION[$key] = $value`).

### The Core Vulnerability: Custom Session Serialization Injection (CRLF Injection)
The vulnerability stems from the complete absence of input sanitization or escaping within the `mywrite` function. The application trustingly accepts user input (such as the `name` parameter) and appends it directly to the multi-line file structural template. 

By injecting a literal carriage return / newline character (`\n` or URL-encoded as `%0A`) into a standard string variable input, an attacker can break out of the intended single-line string boundary. This structurally alters the storage file, appending a discrete new data row that the blind `myread` deserializer treats as an independent, legitimate system variable assignment.

---

## 2. Solution Strategy & Exploitation

### Target Authentication Condition:
To invoke the `print_credentials()` routine and yield the next level password, the deserialized session matrix must satisfy the following strict administrative check:
```php
if($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1)
```

### The Injection Payload Structure:
If we pass a normal payload like `name=alex`, the storage row yields a flat string structure:
```text
name alex
```
The deserializer interprets `name` as the Key, and `alex` as the Value.

However, if we embed a newline (`%0A`) into our input string alongside the targeted administrative key-value payload: `admin%0Aadmin%201`, the internal `mywrite` builder generates an expanded payload block:
```text
name admin
admin 1
```

Upon a subsequent request (or in execution synchronization during a browser submission), the internal sequential parser handles the dataset row-by-row:
1. **Row 1 Parsing**: Evaluates `name admin` → Registers `$_SESSION['name'] = "admin"`.
2. **Row 2 Parsing**: Evaluates `admin 1` → Registers `$_SESSION['admin'] = "1"`.

This implicitly satisfies the privileged control requirement.

### Exploitation via Browser/URL parameter:
Navigate to the application endpoint and directly provide the crafted parameters inside the query string or URL parameter bar to bypass raw HTML multi-line form limitations:
```text
http://natas20.natas.labs.overthewire.org/index.php?name=admin%0Aadmin%201
```

Alternatively, utilizing an implicit multi-line text input field (`<textarea>`) via browser element inspector adjustments or intercepting requests inside a proxy tool allows an exploit injection context to take immediate effect.

## 3. Flag / Final Result
* **Natas Level 21 Password**: `7meHZ1l2zPoK2v1u1TUxq4Ydfjs4U1mU`
