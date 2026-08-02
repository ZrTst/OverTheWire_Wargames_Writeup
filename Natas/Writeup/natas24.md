# OverTheWire: Natas Level 24 -> Level 25 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to bypass an administrative check utilizing a standard string comparison routine and extract the authentication credentials for Natas Level 25.

The entry viewport presents a basic password authentication form field. Evaluating the underlying source file reveals that credential verification relies strictly on the PHP native `strcmp()` function coupled with a logical NOT (`!`) inversion filter:

```php
if(array_key_exists("passwd", \$_REQUEST)){
    if(!strcmp(\$_REQUEST["passwd"], \$thesecret)){
        // 🎯 Privilege Escalation Vector
        echo "<br>The credentials for the next level are:<br>";
    } else {
        echo "<br>Wrong!<br>";
    }
}
```

### The Core Vulnerability: `strcmp()` Type Misalignment & Error-State Overwrite
The `strcmp(string1, string2)` handler is programmatically designed to evaluate and compare exactly two *string type* arguments [🔍](https://php.net). It yields an integer `0` if and only if both strings possess complete structural identity [🔍](https://php.net).

However, in historical legacy PHP runtimes (such as the server container managing this level), passing an improper or complex non-string architecture—specifically an **Array**—as a parameter forces the underlying internal engine into a catastrophic structural exception loop:
1. **The Evaluation Failure**: When `strcmp()` attempts to map a multi-index Array structure against the target flat string file reference (`$thesecret`), the data mismatch causes the function logic to fail entirely [🔍](https://php.net).
2. **The Default Error Return**: Rather than forcing a fatal platform crash, the routine drops a background warning notice and defaults its implicit return value to a blank **`NULL`** primitive [🔍](https://php.net).
3. **The Weak Typing Collapse**: The evaluation chain transfers the `NULL` token back up into the logical conditional check. In PHP's weak type-juggling layer, a `NULL` output is implicitly evaluated as a Boolean **`False`** (0).
4. **The Inversion Bypass**: The preceding exclamation token (`!`) acts on this engine-failure state. Inverting the error-induced `False` (`!False`) transforms the overall execution state into a clear Boolean **`True`**, causing the gate control to drop completely without ever verifying the true secret key.

---

## 2. Solution Strategy & Exploitation

### The Fallacy of Alternative Structural Symbols:
Exploiting this type-mismatch condition requires physical coercion of the variable state during the initial HTTP request parsing cycle. Attempting inputs with other runtime code attributes, such as appending parentheses `?passwd()=`, fails entirely. 

Standard HTTP/URL request architectures classify custom characters like `()` as arbitrary plain-text literals. Rather than execution or variable parsing, it yields a parameter mapping named `"passwd()"`, failing the primary `array_key_exists("passwd")` query constraint before code blocks ever execute.

### Array Coercion via HTTP Parameter Overriding:
To bypass this encoding bottleneck, we leverage PHP’s native web-form query parser feature. Appending **square brackets `[]`** to an active parameter identifier forces the backend's variable allocator to immediately instantiate that variable space as a high-dimension native `Array` layout rather than a standard flat text block.

### Execution Steps (Browser Query Inversion):
1. Navigate directly to the primary level workspace target url:
   `http://natas24.natas.labs.overthewire.org/index.php?passwd=`
2. Focus the top address parameters area and append the explicit array type identifier payload trailing behind the application filename index:
   `http://natas24.natas.labs.overthewire.org/index.php?passwd[]=`
3. Hit Enter to execute.

The server registers the array state, forces `strcmp` to yield `NULL` [🔍](https://php.net), flips the error to `True`, and throws open the password payload directly on the screen text buffer.

---

## 3. Flag / Final Result
* **Natas Level 25 Password**: `UJEF5OAHF1eW3lqkpdCDM7ow4syzh4oo`
