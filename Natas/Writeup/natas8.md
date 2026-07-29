# OverTheWire: Natas Level 8 -> Level 9 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to input the correct secret token to retrieve the password for Natas Level 9. The challenge page provides an input form and allows us to inspect its backend PHP source code. 

By analyzing the source code, we can see that a pre-computed string named `$encodedSecret` is defined, and the user's input is processed through a custom encryption function before comparison. This level tests basic **Reverse Engineering** of a cryptographic encoding pipeline.

## 2. Solution Strategy & Exploitation
The backend source code exposes the exact algorithm used to encrypt the secret:

```php
<?
$encodedSecret = "3d3d516343746d4d6d6c315669563362";

function encodeSecret($secret) {
    return bin2hex(strrev(base64_encode($secret)));
}
// ...
?>
```

The encryption pipeline flows as follows: `Input` -> `Base64 Encode` -> `Reverse String` -> `Bin to Hex` -> `Output`.

To recover the original cleartext secret, we can reverse each operation in the exact opposite order, substituting each function with its corresponding inverse function:
* The inverse of `bin2hex()` is `hex2bin()`
* The inverse of `strrev()` is `strrev()`
* The inverse of `base64_encode()` is `base64_decode()`

### Decryption Script:
We can craft a reverse engineering script in PHP to decrypt the token:

```php
<?php
$encodedSecret = "3d3d516343746d4d6d6c315669563362";

function decodeSecret($encodedSecret) {
    // Reverse the execution pipeline order and operations
    return base64_decode(strrev(hex2bin($encodedSecret)));
}

echo decodeSecret($encodedSecret);
?>
```

### Step-by-step Execution:
1. Run the custom decryption script using an online PHP runner or local environment.
2. The script successfully reverses the operations and outputs the cleartext secret: `oubWYf2kBq`.
3. Return to the main challenge form, enter the decrypted token into the input field, and click **Submit**.

### Result Analysis:
The backend validates the decrypted secret against the hardcoded hash, satisfies the condition, and reveals the flag:
```text
Access granted. The password for natas9 is UdxmI27dTaXmnd1rxKQTfws6jihTdcQ9
```

## 3. Flag / Final Result
* **Natas Level 9 Password**: `UdxmI27dTaXmnd1rxKQTfws6jihTdcQ9`
