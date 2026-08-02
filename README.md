# 🛡️ OverTheWire: Natas Wargame Writeups & Credentials

![Status](https://shields.io)
![Category](https://shields.io)

> 📌 **Project Status**: Actively maintaining Natas level writeups, analyzing vulnerabilities (0-20+), and documenting exploitation techniques.

---

## 🎯 Progress Dashboard (20/34 Levels)

| Level Range | Status | Key Concepts |
| :--- | :---: | :--- |
| **00 - 10** | 🟢 Done | Info Disclosure / XOR / Frontend Flaws |
| **11 - 15** | 🟢 Done | LFI / Boolean-based Blind SQLi / Session Manipulation |
| **16 - 20** | 🟢 Done | Command Injection / Session Hijacking / State Injection |
| **21 - 25** | 🟡 Active| PHP Object Injection / Advanced File Upload Bypass |

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
