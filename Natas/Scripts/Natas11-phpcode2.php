<?php
$key = "KBSw";
// 伪造目标明文
$malicious_data = json_encode(array("showpassword"=>"yes", "bgcolor"=>"#ffffff"));

// 使用还原出的密钥进行加密
$ciphertext = "";
for($i = 0; $i < strlen($malicious_data); $i++) {
    $ciphertext .= $malicious_data[$i] ^ $key[$i % strlen($key)];
}

// 重新进行 Base64 编码
echo "伪造的 Cookie: " . base64_encode($ciphertext) . "\n";
?>
