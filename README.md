# 🔐 CryptoShare AI 

> **Premium Zero-Knowledge Secure File Sharing Platform.**

CryptoShare AI is a modern, enterprise-grade SaaS web application built to solve the vulnerabilities of file transmission. Utilizing a robust Python backend with AES-128 encryption and an elegant, responsive glassmorphism UI, this application ensures your payloads remain completely private.

## ✨ Core Features

* **Zero-Knowledge Architecture:** Files are encrypted immediately upon upload. The server discards the raw file and never stores the decryption key.
* **Burn After Reading:** The moment a payload is successfully decrypted, the cipher file is permanently wiped from the server hardware.
* **Time-to-Live (TTL):** Automated 24-hour expiration protocol ensures abandoned files are securely destroyed.
* **AI Heuristic Risk Scoring:** Simulates risk-assessment by analyzing file extensions and scoring potential payload threats.
* **Out-of-Band Key Exchange:** The system separates the Magic Link and Decryption Key, mandating multi-channel verification.
* **Premium UI/UX:** Features a Stripe/Linear-inspired light-mode interface with frosted glassmorphism, smooth animations, and real-time AJAX progress tracking.

## 🛠️ Tech Stack

* **Backend:** Python, Flask, Werkzeug
* **Cryptography:** `cryptography.fernet` (AES in CBC mode)
* **Frontend:** HTML5, CSS3 (Custom Glassmorphism), Vanilla JS
* **Utilities:** QRCode.js for mobile-handoff

## 🚀 Installation & Deployment

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/CryptoShare-AI.git](https://github.com/yourusername/CryptoShare-AI.git)
   cd CryptoShare-AI

---

 **Made by Kinza Zahra**

