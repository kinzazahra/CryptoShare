import os
from flask import Flask, render_template, request, send_file, after_this_request, session, redirect, url_for
from cryptography.fernet import Fernet
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)

# Configurations
app.secret_key = "super_secret_hackathon_key" 
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Mock Database for Login
VALID_USER = "admin"
VALID_PASS = "secure123"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == VALID_USER and password == VALID_PASS:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = "Invalid Credentials. Try again."
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return {"error": "No file uploaded"}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {"error": "No file selected"}, 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    with open(filepath, 'rb') as f:
        file_data = f.read()

    encrypted_data = cipher_suite.encrypt(file_data)
    enc_filename = filename + '.enc'
    enc_filepath = os.path.join(app.config['UPLOAD_FOLDER'], enc_filename)

    with open(enc_filepath, 'wb') as f:
        f.write(encrypted_data)

    os.remove(filepath)

    # 🔥 THE UPGRADE: Generate the full Magic Link
    magic_link = request.host_url + 'download/' + enc_filename

    return {
        "filename": enc_filename,
        "key": key.decode('utf-8'),
        "link": magic_link,
        "message": "File encrypted successfully!"
    }

# 🔥 NEW ROUTE: The Public Magic Link Page
@app.route('/download/<filename>')
def download_page(filename):
    enc_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Check if file has already been burned
    if not os.path.exists(enc_filepath):
        return render_template('burned.html')
        
    return render_template('download.html', filename=filename)

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    filename = request.form.get('filename')
    key = request.form.get('key')
    
    if not filename or not key:
        return "Missing file or key", 400

    enc_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(enc_filepath):
        return "<h2>Error 404</h2><p>File not found. It has already been destroyed.</p>", 404

    try:
        cipher_suite = Fernet(key.encode('utf-8'))
        
        with open(enc_filepath, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = cipher_suite.decrypt(encrypted_data)
        
        dec_filename = "decrypted_" + filename.replace('.enc', '')
        dec_filepath = os.path.join(app.config['UPLOAD_FOLDER'], dec_filename)

        with open(dec_filepath, 'wb') as f:
            f.write(decrypted_data)

        os.remove(enc_filepath) # Burn After Reading

        @after_this_request
        def remove_file(response):
            try:
                os.remove(dec_filepath)
            except Exception as error:
                app.logger.error("Error removing file", error)
            return response

        return send_file(dec_filepath, as_attachment=True)
    
    except Exception as e:
        return f"<h2>Decryption Failed!</h2><p>Invalid Key or Corrupted File. Go back and try again.</p>", 400

if __name__ == '__main__':
    app.run(debug=True)