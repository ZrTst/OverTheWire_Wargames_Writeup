<?php
// 1. 抓包或在浏览器中看到的默认 Cookie 密文
$cookie_ciphertext = "EGAgHwQ1IxYYMSQYGSZxTUksPFVHYDEQCC0%2FGBlgaVVIJDURDSQ1VRY%3D";

// 2. 对应的已知明文 JSON
$malicious_data = json_encode(array("showpassword"=>"yes", "bgcolor"=>"#ffffff"));

// 3. 执行异或运算还原密钥
$raw_ciphertext = base64_decode($cookie_ciphertext);
$key = "";

for($i = 0; $i < strlen($raw_ciphertext); $i++) {
    $key .= $raw_ciphertext[$i] ^ $plaintext[$i % strlen($plaintext)];
}

echo "循环生成的密钥流: " . $key . "\n";
?>
