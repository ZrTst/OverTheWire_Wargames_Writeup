# OverTheWire: Natas Level 11 -> Level 12 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to compromise the session management system to retrieve the password for Natas Level 12. The application stores user preferences (like background color) inside a session cookie encrypted via a custom XOR implementation. 

By analyzing the provided source code, we can audit the cryptographic strength of this routine.

### Source Code Review:
```php
function xor_encrypt($in) {
    $key = '<censored>';
    $text = $in;
    $outText = '';

    for($i=0;$i<strlen($text);$i++) {
        $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}
```
The application uses a stream cipher based on cyclical XOR encryption. In cryptography, XOR operation is completely symmetrical. If `Plaintext ^ Key = Ciphertext`, then mathematically `Plaintext ^ Ciphertext = Key`. 

Since the application initializes a default state array `array("showpassword"=>"no", "bgcolor"=>"#ffffff")` and sends its Base64-encoded encrypted string to the client, we have access to both the raw plaintext and the matching ciphertext. This exposes the routine to a classic **Known-Plaintext Attack (KPA)** to recover the secret key.

## 2. Solution Strategy & Exploitation

### Step 1: Recovering the Secret Key
We capture the default Base64 cookie string from the browser: `EGAgHwQ1IxYYMSQYGSZxTUk7NgRJbnEVDCE8GwQwcU1JYTURDSQ1EUk%2F`. After decoding it, we write a quick PHP script to XOR the known default JSON plaintext against the recovered ciphertext bytes:

```php
<?php
$plain_text = json_encode(array("showpassword"=>"no", "bgcolor"=>"#ffffff"));
$cookie_b64 = "EGAgHwQ1IxYYMSQYGSZxTUk7NgRJbnEVDCE8GwQwcU1JYTURDSQ1EUk%2F";
$cipher_text = base64_decode($cookie_b64);

$key = "";
for($i=0; $i<strlen($plain_text); $i++) {
    $key .= $plain_text[$i] ^ $cipher_text[$i];
}
echo "Recovered Key Stream: " . $key;
?>
```
**Execution Output:**
The script prints a repeating string pattern: `kBSwkBSwkBSwkBSwk...`. This confirms that the underlying secret hardcoded key is a 4-byte string: **`kBSw`**.

### Step 2: Forging the Session Cookie
Now that the key is known, we can manipulate the parameter state to flip `"showpassword"` from `"no"` to `"yes"`. We construct our forged plaintext array: `{"showpassword":"yes","bgcolor":"#ffffff"}` and run an encryption script using the recovered key:

```php
<?php
$key = 'kBSw'; 
$modified_plaintext = '{"showpassword":"yes","bgcolor":"#ffffff"}';

$outText = '';
for($i = 0; $i < strlen($modified_plaintext); $i++) {
    $outText .= $modified_plaintext[$i] ^ $key[$i % strlen($key)];
}

$payload_cookie = base64_encode($outText);
echo "Forged Cookie: " . $payload_cookie;
?>
```
**Execution Output:**
```text
Forged Cookie: MGg7CgAxORgYPTwXKTAlSFA7NgRJbnEVDCE8GwQwcU1JYTURDSQ1EUk/
```

### Step-by-step Execution:
1. Open the browser's Developer Tools (F12) and head to the **Application / Storage** tab.
2. Under **Cookies**, select the Natas 11 domain.
3. Replace the original session cookie value with our newly generated payload: `EGAgHwQ1IxYYMSQYGSZxTUk7NgRJbnEVDCE8GwQwcU1JYTURDSQ1EUk/`.
4. Refresh the page (`F5`) to transmit the tampered state token.

### Result Analysis:
The server decrypts the payload successfully using its internal key, interprets the forged state `showpassword => yes`, bypasses the access block, and renders the flag:
```text
The password for natas12 is EAGkE8uzFTxeoTT2mMst9Xy7PX6guEng
```

## 3. Flag / Final Result
* **Natas Level 12 Password**: `EAGkE8uzFTxeoTT2mMst9Xy7PX6guEng`
