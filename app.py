import os
import time
from flask import Flask, render_template, request, send_file, after_this_request, session, redirect, url_for, jsonify
from cryptography.fernet import Fernet
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)

# --- CONFIGURATIONS ---
app.secret_key = "cryptoshare_enterprise_secure_key"
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB Max limit
app.config['FILE_TTL'] = 86400  # 24 Hours Time-to-Live

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- MOCK ADMIN DB ---
VALID_USER = "admin"
VALID_PASS = "secure123"

# --- AI HEURISTICS MOCK ENGINE ---
def analyze_file_risk(filename):
    """Simulates an AI heuristic scan for suspicious extensions."""
    high_risk_exts = ['.exe', '.bat', '.sh', '.vbs', '.scr']
    ext = os.path.splitext(filename)[1].lower()
    if ext in high_risk_exts:
        return {"risk_score": 85, "status": "High Risk", "color": "red"}
    elif ext in ['.zip', '.rar', '.tar']:
        return {"risk_score": 40, "status": "Medium Risk", "color": "orange"}
    return {"risk_score": 12, "status": "Safe", "color": "green"}

# --- AUTH DECORATOR ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROUTES ---

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == VALID_USER and password == VALID_PASS:
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    return render_template('index.html', error="Invalid Credentials")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Apply AI Risk Analysis
    risk_profile = analyze_file_risk(filename)

    # Encrypt
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    with open(filepath, 'rb') as f:
        file_data = f.read()

    encrypted_data = cipher_suite.encrypt(file_data)
    enc_filename = filename + '.enc'
    enc_filepath = os.path.join(app.config['UPLOAD_FOLDER'], enc_filename)

    with open(enc_filepath, 'wb') as f:
        f.write(encrypted_data)

    os.remove(filepath) # Destroy raw file

    magic_link = request.host_url + 'download/' + enc_filename

    return jsonify({
        "filename": enc_filename,
        "key": key.decode('utf-8'),
        "link": magic_link,
        "risk_profile": risk_profile,
        "message": "Payload Secured"
    })

@app.route('/download/<filename>')
def download_page(filename):
    enc_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(enc_filepath):
        return render_template('error.html', message="Payload has been destroyed or never existed.")
        
    file_age = time.time() - os.path.getmtime(enc_filepath)
    if file_age > app.config['FILE_TTL']:
        os.remove(enc_filepath)
        return render_template('error.html', message="Link Expired. Payload securely wiped.")
        
    return render_template('download.html', filename=filename)

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    filename = request.form.get('filename')
    key = request.form.get('key')
    
    if not filename or not key:
        return render_template('error.html', message="Missing file or key data."), 400

    enc_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(enc_filepath):
        return render_template('error.html', message="File not found. It has already been destroyed."), 404

    try:
        cipher_suite = Fernet(key.encode('utf-8'))
        
        with open(enc_filepath, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = cipher_suite.decrypt(encrypted_data)
        
        dec_filename = "decrypted_" + filename.replace('.enc', '')
        dec_filepath = os.path.join(app.config['UPLOAD_FOLDER'], dec_filename)

        with open(dec_filepath, 'wb') as f:
            f.write(decrypted_data)

        # 🔥 BURN AFTER READING
        os.remove(enc_filepath) 

        @after_this_request
        def remove_file(response):
            try:
                os.remove(dec_filepath)
            except Exception as error:
                app.logger.error("Error removing temp file", error)
            return response

        return send_file(dec_filepath, as_attachment=True)
    
    except Exception as e:
        return render_template('error.html', message="Decryption Failed. Invalid Key or Corrupted Payload."), 400

if __name__ == '__main__':
    app.run(debug=True)