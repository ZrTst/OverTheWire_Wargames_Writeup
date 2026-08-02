# 🛡️ OverTheWire: Natas Wargame Writeups & Credentials

![Status](https://shields.io)
![Category](https://shields.io)

> 📌 **Project Status**: Actively maintaining Natas level writeups, analyzing vulnerabilities (0-20+), and documenting exploitation techniques.

---

## 🎯 Progress Dashboard (20/34 Levels)

## 🎯 Progress Dashboard (20/34 Levels Mastered)

| Level Range | Status | Key Security Concepts & Vulnerabilities |
| :--- | :---: | :--- |
| **00 - 10** | 🟢 Done | Information Disclosure / Source Code Auditing / XOR Crypto / Frontend Flaws |
| **11 - 15** | 🟢 Done | Arbitrary File Inclusion (LFI) / Blind SQLi / Session Manipulation |
| **16 - 20** | 🟢 Done | Command Injection / Advanced Session Hijacking / Server-Side State Injection |
| **21 - 25** | 🟡 Active | PHP Object Injection / Directory Traversal Bypasses / Log Injection |
| **26 - 27** | 🔵 Planned | Object Serialization Exploits / Race Conditions / Dual-Query Blind Appends |
| **28 - 30** | 🪓 Planned | Advanced SQLi (Byte Manipulation) / Information Leak via String Truncation |
| **31 - 34** | 💀 Hardcore | Complex Code Auditing / Node.js & Advanced Python Exploitation / Final Bosses |

---

## 🛠️ Repository Highlights

- **Custom Exploitation**: All payloads are built using Python/Requests, avoiding reliance on automated tools to deeply understand vulnerability mechanisms.
- **Efficiency Focus**: Implemented Binary Search Algorithms for blind SQLi, reducing request overhead and optimizing exploit speed.
- **Robustness**: Includes exception handling and state management for reliable execution.

---

## 📂 Repository Structure

```text
├── Natas/
│   ├── natas15/
│   │   ├── writeup.md    # Detailed RCA & remediation
│   │   └── exploit.py    # Custom binary search SQLi
│   ├── natas18/
│   │   └── ...
└── README.md
```

---

## ⚠️ Legal Disclaimer
For educational purposes only. Validated strictly within OverTheWire.
