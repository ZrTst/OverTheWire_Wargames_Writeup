# 🎮 OverTheWire Wargames Complete Writeups & Automation

![Repo Size](https://img.shields.io/github/repo-size/ZrTst/OverTheWire_Wargames_Writeup?style=for-the-badge&color=2E3440&labelColor=1A1C23)
![Last Commit](https://img.shields.io/github/last-commit/ZrTst/OverTheWire_Wargames_Writeup?style=for-the-badge&color=BF616A&labelColor=1A1C23)
![Top Language](https://img.shields.io/github/languages/top/ZrTst/OverTheWire_Wargames_Writeup?style=for-the-badge&color=EBCB8B&labelColor=1A1C23)

Welcome to my repository featuring complete writeups and automation exploit scripts for various OverTheWire cyber security wargames. This project focuses on pure, hand-crafted exploit development, rejecting blind reliance on automated tools. The goal is to deeply dissect the core mechanisms of Web Security, System Security, and Reverse Engineering.

---

## 🗺 Wargames Navigation

This repository is structured as a **Monorepo**. Each wargame series has its own independent subdirectory and dedicated README. Click the links below to view the progress and source code for each series:

| Wargame | Core Security Domain | Current Progress | Documentation Link |
| :--- | :--- | :--- | :--- |
| **Natas** | Web Application Security | 🟢 20 / 34 | [Go to Natas Writeups ➔](./Natas/README.md) |
| **Bandit** | Linux CLI Basics & System Security | ⚪ ⏳ Pending | [Go to Bandit Writeups ➔](./Bandit/README.md) |

*(Note: As I complete other series, corresponding subfolders will be created, and this navigation table will be updated simultaneously.)*

---

## 🛠 Tech Stack & Design Principles

* **Hand-Crafted Payloads**: Built primarily using **Python / Requests** or native Bash scripts to ensure complete control over packet structures.
* **Algorithmic Efficiency**: Features **Binary Search algorithms** in blind exploitation scenarios (like Blind SQLi) to minimize request overhead and latency.
* **Robust Architecture**: All automation scripts include comprehensive exception handling and state persistence management to ensure reliability during batch validation.

---

## 📂 Repository Directory Tree

```text
.
├── Bandit/               # Linux basics & system security (Planned)
└── Natas/                # Web application security (Current Focus)
    ├── Scripts/          # Automation exploit scripts (Python/Bash)
    ├── Writeup/          # Detailed vulnerability analysis & walkthroughs
    └── README.md         # Dedicated progress dashboard for Natas
```

---

## ⚠ Legal Disclaimer

All technical analyses, exploit payloads, and automation scripts contained in this repository are **strictly for defensive educational purposes and academic research**. All technical validations are executed within the officially authorized and legal sandbox environment provided by OverTheWire. Do not use these assets against any unauthorized production systems or for illegal penetration testing. The user assumes full legal responsibility for any direct or indirect consequences arising from misuse.

---

© 2026 ZrTst. Built with Passion for Cyber Security.
