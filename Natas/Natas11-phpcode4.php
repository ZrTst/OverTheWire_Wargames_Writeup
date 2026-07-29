<?php
// 1. 你的默认明文（数组 JSON 化后的样子）
$plain_text = json_encode(array("showpassword"=>"no", "bgcolor"=>"#ffffff"));

// 2. 你的默认密文（去你的浏览器里复制那一串 data Cookie，填在下面替换 CladXXXX）
$cookie_b64 = "填入你浏览器里复制出来的Cookie值";
$cipher_text = base64_decode($cookie_b64);

// 3. 还原 Key
$key = "";
for($i=0; $i<strlen($plain_text); $i++) {
    $key .= $plain_text[$i] ^ $cipher_text[$i];
}
echo "大功告成，隐藏的 Key 是: " . $key;
?>

