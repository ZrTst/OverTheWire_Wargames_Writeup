# OverTheWire: Natas Level 16 -> Level 17 Writeup

## 1. Challenge Background & Source Code Analysis
The challenge provides a search filtering functionality. Upon reviewing the backend source code, the critical filtering logic is found as follows:

```php
if(preg_match('/[;|&`\'"]/', $key)) {
    // Filters common delimiters, backticks, and quotes
}
```

## 2. Solution Strategy (Bypass Analysis)
Although the code uses `preg_match` to filter characters such as `;`, `|`, `&`, `` ` ``, `'`, and `"`, it **misses `$(...)` (Command Substitution)**.

In Bash, `$(command)` executes the command inside the parentheses first and uses its output as an argument for the outer command.

### Boolean-based Blind Command Injection Principle
We can construct the following input:
```bash
$(grep ^a /etc/natas_webpass/natas17)
```

The actual command concatenated and executed by the backend becomes:
```bash
grep -i $(grep ^a /etc/natas_webpass/natas17) dictionary.txt
```

The page response follows this **Boolean logic**:
1. **Match Successful (True)**: If the password in `/etc/natas_webpass/natas17` starts with the letter `a`, the inner `grep` returns the password string. Since `dictionary.txt` is highly unlikely to contain this high-entropy password, the outer `grep` finds no matches. Consequently, **the page will display nothing (no output)**.
2. **Match Failed (False)**: If the password does not start with `a`, the inner `grep` returns an empty string. The outer command downgrades to a search with no pattern, causing the entire contents of `dictionary.txt` to be printed. As a result, **the page will show a large amount of output**.

By utilizing this inverse Boolean characteristic ("output means False, no output means True"), we can perform a blind injection.

## 3. Automation Script
We can write an automated brute-force script in Python to guess the `natas17` password character by character (including uppercase letters, lowercase letters, and digits):
*Refer to /Writeup/Natas16-pycode.py*
## 4. Flag / Final Result
After running the automation script, the password for the next level was successfully retrieved:
```text
KLdAM3VZux8o6TbkbhuaG5KtYjI77tfx
```
