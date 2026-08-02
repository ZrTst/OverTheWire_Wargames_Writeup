# OverTheWire: Natas Level 23 -> Level 24 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to provide a specific password string parameter (`passwd`) that simultaneously satisfies two seemingly contradictory logical constraints to unlock the credentials for Natas Level 24.

Upon evaluating the backend PHP source code, the primary security control relies on a conditional block paired with a logical AND (`&&`) operator:

```php
if(array_key_exists("passwd", \$_REQUEST)){
    if(strstr(\(_REQUEST["passwd"], "iloveyou") && (\)_REQUEST["passwd"] > 10 )){
        // 🎯 Privilege Escalation Vector
        echo "<br>The credentials for the next level are:<br>";
    } else {
        echo "<br>Wrong!<br>";
    }
}
```

### The Core Vulnerability: PHP Type Juggling & Loose String-to-Integer Conversion
An initial or casual observation of the source code might lead an attacker to simply input `iloveyou` to pass the first string-matching condition (`strstr`). However, doing so fails the second numeric constraint (`$_REQUEST["passwd"] > 10`), causing the application to return "Wrong!".

The critical flaw stems from PHP’s legacy loose-typing architecture and its automated type conversion (Type Juggling) rules [🔍](https://php.net):
* **String-to-Integer Coercion Mechanics**: When a string operand is compared against a literal integer using a numeric relational operator (such as `>`), the PHP runtime engine forces the string to implicitly cast into a numeric representation.
* **The Numeric Extractor Behavior**: PHP parses the target string starting strictly from the *first character* moving left-to-right. 
  * If the string initiates with valid numeric digits, it extracts those prefix digits as an integer value and **silently discards all trailing alphabetic characters**.
  * If the string initiates with non-numeric characters, the extractor fails entirely and defaults the evaluation of the entire string asset to integer `0`.

---

## 2. Solution Strategy & Exploitation

### Crafting the Multi-Modal Hybrid Payload
To defeat this loose type-checking pipeline, we must construct a hybrid string that masquerades as a numeric value to the math engine while maintaining its textual substrate for the string matcher.

By passing a payload structured as `[Numeric Prefix] + [Text Substrate]`, specifically **`11iloveyou`**, we weaponize both halves of the logical check:

1. **Sub-Condition 1 Evaluation (`strstr`)**:
   The routine evaluates `strstr("11iloveyou", "iloveyou")`. The query needle `"iloveyou"` is successfully located inside the haystack string, resolving to a Boolean **True**.
2. **Sub-Condition 2 Evaluation (`> 10`)**:
   The routine evaluates `"11iloveyou" > 10`. The PHP type-juggling layer detects the integer `10` and triggers an implicit cast on the left operand. It reads the prefix `11`, immediately throws away the trailing alpha text `"iloveyou"`, and translates the math operation internally to `11 > 10`, which logically resolves to a Boolean **True**.

Since both states yield **True && True**, the enforcement block collapses.

### Execution Steps (Direct Form Interaction):
Because the payload is natively supported by plain URL and form data streams, automation scripts are entirely redundant for this level.

1. Navigate to the primary challenge interface: `http://natas23.natas.labs.overthewire.org/?passwd=11iloveyou`
2. Locate the input field mapping to the `passwd` parameter block.
3. Inject the crafted type-juggling payload: `11iloveyou` (any numeric prefix integer larger than 10, such as `100iloveyou`, functions identically).
4. Click the "Login" form submission action button.

The application instantly prints the hidden administrative authentication payload on the primary active viewport canvas.

---

## 3. Flag / Final Result
* **Natas Level 24 Password**: `shlL4BvOtawNCd81dwdKRHFzmTEjYYQX`
