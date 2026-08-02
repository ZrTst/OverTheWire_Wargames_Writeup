# OverTheWire: Natas Level 14 -> Level 15 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to bypass an authentication form to retrieve the password for Natas Level 15. The page provides a login interface consisting of username and password fields and exposes its backend PHP source code. 

By analyzing the source code, we can inspect how the application handles database queries.

### Source Code Review:
The application constructs the backend database query using direct string concatenation:
```php
$query = "SELECT * from users where username=\"" . $_REQUEST["username"] . "\" and password=\"" . $_REQUEST["password"] . "\"";
```
The user inputs are enclosed in double quotes (`"`) and directly embedded into the SQL command without any sanitization or parameterized queries (Prepared Statements). This architecture introduces a classic and critical **SQL Injection (SQLi)** vulnerability.

## 2. Solution Strategy & Exploitation
To bypass the login restriction, we can perform an authentication bypass attack. In SQL, the `OR` operator evaluates to true if either condition is true. If we can manipulate the query logic so that the `WHERE` clause always returns true, the database will return the first record found (usually the administrative or specified account), authorizing the login session regardless of the password supplied.

### Payload Construction:
By inputting the following string into the `username` field (incorporating a SQL comment character `#` to truncate the remainder of the backend query):
```sql
natas15" or "1"="1" #
```
And leaving the `password` field arbitrary, the backend SQL statement expands into:
```sql
SELECT * from users where username="natas15" or "1"="1" #" and password="..."
```

### Logical Breakdown:
1. The database processes the criteria up to the `#` symbol; everything following it is treated as a comment and discarded by the SQL parser.
2. The remaining active expression becomes `username="natas15" OR "1"="1"`.
3. Since `"1"="1"` is a tautology (always `True`), the `OR` condition forces the entire `WHERE` clause to evaluate to `True`, bypassing the password validation layer entirely.

### Step-by-step Execution:
1. Access the challenge login page.
2. In the **Username** input box, enter the crafted payload: `natas15" or "1"="1 #`.
3. Leave the **Password** field empty or input any dummy text.
4. Click the **Login** button.

### Result Analysis:
The database processes the altered logical condition, bypasses the credential verification layer entirely, and displays the next level's secret flag:
```text
Successful login! The password for natas15 is GB6USCJYJjwLyYhZUNkE1NwDueiTow6g
```

## 3. Flag / Final Result
* **Natas Level 15 Password**: `GB6USCJYJjwLyYhZUNkE1NwDueiTow6g`
