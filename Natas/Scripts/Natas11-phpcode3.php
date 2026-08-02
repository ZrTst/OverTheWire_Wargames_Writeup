<?php
// 1. 确保你的注入 Cookie 没有任何空格
$my_cookie = "ClVLIh4ASCsCBE8lAxMacFMOXTlTWxooFhRXJh4FGnBTVF4sFxFeLFMK";

// 2. 目标关卡网址
$url = "http://overthewire.org";

// 3. 配置带 Cookie 和验证信息的请求
$options = array(
    'http' => array(
        'method' => "GET",
        // 关键：这里需要严格填入你进入 natas11 网页时弹窗输入的账号密码
        // 格式为 base64_encode("用户名:密码")
        'header' => "Cookie: data=" . $my_cookie . "\r\n" .
                    "Authorization: Basic " . base64_encode("natas11:VUMQDmuITOEHzhviLE5V0VG9cPMQkyxd") . "\r\n" .
                    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n",
        'follow_location' => false // 阻止它自动跳到 /wargames/
    )
);

$context = stream_context_create($options);
$response = file_get_contents($url, false, $context);

// 4. 清洗输出，只打印出含有密码或关键信息的部分
if ($response === FALSE) {
    echo "请求失败，请检查网络或密码！\n";
} else {
    echo "--- 成功获取网页内容 ---\n";
    // 打印包含 password 的行
    if (preg_match('/The password for natas12 is .*/', $response, $matches)) {
        echo "\033[32m" . $matches[0] . "\033[0m\n";
    } else {
        // 如果没匹配到，打印前20行看看服务器到底返回了什么
        echo substr($response, 0, 1000);
    }
}
?>
