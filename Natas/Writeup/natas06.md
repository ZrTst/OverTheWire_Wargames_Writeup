# OverTheWire: Natas Level 6 -> Level 7 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to submit the correct secret token to retrieve the password for Natas Level 7. The main page presents an input form asking for a "Secret". 

However, the application exposes a link to its backend implementation, allowing us to perform a **Source Code Review (White-box Auditing)** to trace the validation logic and identify potentially exposed include files or configurations.

## 2. Solution Strategy & Exploitation
By reviewing the PHP implementation, we can analyze how the server-side code handles the authentication check and where the verification data resides.

### Source Code Review:
The source code at `index-source.html` reveals the following critical PHP block:
```php
<?
include "includes/secret.inc";

if(array_key_exists("submit", $_POST)) {
    if($secret == $_POST['secret']) {
        print "Access granted. The password for natas7 is <censored>";
    } else {
        print "Wrong secret";
    }
}
?>
```
The comparison logic evaluates the user input against a variable named `$secret`. Crucially, this variable is not defined within the main script but is instead imported from an external configuration file located at `includes/secret.inc`. 

If the web server does not restrict direct access to the `includes/` directory or its subfiles, we can intercept the hardcoded credential directly.

### Step-by-step Execution:
1. Identify the location of the secret resource from the code: `includes/secret.inc`.
2. Construct and navigate to the direct file path via the browser URL bar:
   ```text
   http://natas6.natas.labs.overthewire.org/includes/secret.inc
   ```
3. Inspect the raw source of the loaded configuration file to find the hardcoded PHP variable definition:
   ```php
   <?
   $secret = "FOEIUWGHFEEUHOFUOIU";
   ?>
   ```
4. Return to the main challenge form, enter `FOEIUWGHFEEUHOFUOIU` into the input field, and click **Submit**.

### Result Analysis:
The backend validates the correct token, satisfies the conditional block, and prints the flag:
```text
Access granted. The password for natas7 is B1szg95UcTnrzwnF3i3TzYHlyYh8iBV0
```

## 3. Flag / Final Result
* **Natas Level 7 Password**: `B1szg95UcTnrzwnF3i3TzYHlyYh8iBV0`
