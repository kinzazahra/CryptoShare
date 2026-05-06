# 🔐 CryptoShare AI

> **Enterprise-Grade, Zero-Knowledge, Self-Destructing File Gateway.**

CryptoShare AI is a secure file-transfer web application designed to solve the vulnerabilities of sharing sensitive files over standard messaging platforms (like WhatsApp, Slack, or Email). It utilizes **Symmetric Cryptography (AES)** and an **Out-of-Band Key Exchange** methodology to ensure true zero-knowledge file hosting.

## ✨ Key Features

* **🔥 Burn After Reading:** The moment a receiver successfully decrypts and downloads a file, the encrypted payload is permanently wiped from the server hardware. 
* **🪄 Magic Links:** Generates a clean, unique URL for the receiver to access the decryption portal, simulating a WeTransfer/Dropbox experience.
* **🛡️ Zero-Knowledge Architecture:** The server encrypts the file immediately upon upload and drops the raw file. The server *never* stores the decryption key.
* **🔑 Out-of-Band Exchange:** Designed so the Sender transmits the Magic Link and the Decryption Key via separate channels (e.g., Link via Email, Key via SMS) to prevent man-in-the-middle attacks.
* **💻 Admin Access Control:** Uploads are strictly locked behind an admin portal to prevent public server-storage abuse, while downloads remain frictionless for the public.
* **🖱️ Modern UX:** Features a responsive, drag-and-drop user interface built with vanilla HTML/CSS/JS.

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Cryptography:** `cryptography.fernet` (AES in CBC mode with a 128-bit key)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (AJAX)

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/CryptoShare-AI.git](https://github.com/yourusername/CryptoShare-AI.git)
   cd CryptoShare-AI
Install the required dependencies:
Make sure you have Python installed, then run:

Bash
pip install flask cryptography werkzeug
Run the application:

Bash
python app.py
Access the portal:
Open your browser and navigate to http://127.0.0.1:5000

📖 How to Use
For the Sender (Admin)
Go to the web app; you will be redirected to the secure login page.

Log in using the default admin credentials:

Username: admin

Password: secure123

Drag and drop a sensitive file into the upload zone and click Encrypt & Generate Link.

The system will output two things:

A Magic Link (Send this to your recipient).

A 44-Character Secret Key (Send this to your recipient via a different secure channel).

For the Receiver (Public)
The receiver clicks the Magic Link.

They are greeted by a clean, self-destruct warning page.

They paste the Secret Key into the input box and click Unlock & Download.

The file decrypts in memory, downloads to their machine, and the server permanently deletes the .enc file. The link will now return a 404 Error if clicked again.

🧠 Security Methodology (Hackathon Notes)
This project was built with a Zero-Trust mindset. If a malicious actor compromises the server, they will only find .enc files consisting of scrambled ciphertexts. Because the decryption keys are generated locally and immediately handed off to the user (never stored in a database), the server itself cannot decrypt the files it hosts.

Built for Hackathons & Secure Communications.

