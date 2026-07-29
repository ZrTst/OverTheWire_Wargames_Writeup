# OverTheWire: Natas Level 13 -> Level 14 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to retrieve the password for Natas Level 14. The web application features a file upload form similar to the previous level, but with an upgraded backend verification layer to enforce security. 

By reviewing the source code, we observe that the server now validates the uploaded file using the PHP `exif_imagetype()` function:

```php
if (!exif_imagetype($_FILES['uploadedfile']['tmp_name'])) {
    echo "File is not an image";
}
```

The `exif_imagetype()` function inspects the first few bytes of a file, known as **Magic Bytes** or the file signature, to determine its actual type. Simply renaming a file extension will no longer bypass this check, as a pure text PHP script will lack a valid image signature and be rejected.

## 2. Solution Strategy & Exploitation
To bypass this restriction, we can craft a polyglot file—a file that satisfies the signature of a valid image format while containing malicious PHP payload code. 

For instance, the magic bytes for a GIF file in ASCII are `GIF89a` (hex: `47 49 46 38 39 61`). If we prepend `GIF89a` to our PHP WebShell, `exif_imagetype()` will identify the file as a valid GIF image. Concurrently, when the web server executes the file via the PHP interpreter, the `GIF89a` string will be treated as plain output text, and the subsequent PHP code block will be parsed and executed.

### WebShell Payload Construction:
We prepend the GIF magic bytes directly into our system command execution script:
```php
GIF89a
<?php
system('cat /etc/natas_webpass/natas14');
?>
```

### Step-by-step Execution:
1. Save the payload code above locally as a file (e.g., `Natas13-phpcode.php`).
2. Access the challenge upload page.
3. Open the browser's **Developer Tools (F12)** and inspect the form elements.
4. Locate the vulnerable hidden input field managing the final filename and extension:
   ```html
   <input type="hidden" name="filename" value="[random_string].jpg" />
   ```
5. Modify the `value` attribute to force a `.php` file extension (e.g., `payload.php`).
6. Browse and select your crafted `Natas13-phpcode.php` file, then click the **Upload** button.
7. The server-side `exif_imagetype()` reads the `GIF89a` header, accepts it as a valid image, and saves it with our requested `.php` extension.
8. Click the generated file link to view the execution output.

### Result Analysis:
The server loads the file, spits out the raw text header `GIF89a`, immediately processes the embedded PHP block to dump the password store, and reveals the flag:
```text
GIF89a A0xXu2x9FW8rb8OSQ4ei6n5VBbLUz8h8
```

## 3. Flag / Final Result
* **Natas Level 14 Password**: `A0xXu2x9FW8rb8OSQ4ei6n5VBbLUz8h8`
