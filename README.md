# 🛡️ Sentinel-Web: Advanced Vulnerability Scanner

![Version](https://img.shields.io/badge/Version-3.0-blue) ![Python](https://img.shields.io/badge/Python-3.x-green) ![Security](https://img.shields.io/badge/Focus-Web%20Security-red)

**Sentinel-Web** is an interactive, automated vulnerability scanner designed to detect **Cross-Site Scripting (XSS)** and **Blind SQL Injection (SQLi)** in web applications.

It features a **CamPhish-style interactive menu**, making it easy for anyone to use without memorizing commands.

---

## 🚀 Key Features

* **Interactive Mode:** Just run the tool and follow the on-screen menu.
* **Smart Payload Injection:** Automatically detects if the target needs String (`'`) or Integer-based payloads.
* **Blind SQLi Detection:** Uses heuristic time-based analysis (`SLEEP(5)`) to find hidden vulnerabilities where no error messages are displayed.
* **Bulk Scanning:** Can scan multiple websites from a text file.

---

## 🛠️ Installation & Usage

1. **Clone the Tool**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Sentinel-Web.git](https://github.com/YOUR_USERNAME/Sentinel-Web.git)
   cd Sentinel-Web
2.**nstallRequirements**
```bash
  pip install -r requirements.txt

3.**Run the Tool**
```bash
python scanner.py
