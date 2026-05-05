import os
from flask import Flask, render_template, request, send_file
from cryptography.fernet import Fernet
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Configurations
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {"error": "No file uploaded"}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {"error": "No file selected"}, 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # 1. Generate a symmetric encryption key
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    # 2. Read the original file
    with open(filepath, 'rb') as f:
        file_data = f.read()

    # 3. Encrypt the data
    encrypted_data = cipher_suite.encrypt(file_data)
    enc_filename = filename + '.enc'
    enc_filepath = os.path.join(app.config['UPLOAD_FOLDER'], enc_filename)

    # 4. Save the encrypted file
    with open(enc_filepath, 'wb') as f:
        f.write(encrypted_data)

    # 5. Delete the original unencrypted file for security!
    os.remove(filepath)

    return {
        "filename": enc_filename,
        "key": key.decode('utf-8'),
        "message": "File encrypted successfully!"
    }

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    filename = request.form.get('filename')
    key = request.form.get('key')
    
    if not filename or not key:
        return "Missing file or key", 400

    enc_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(enc_filepath):
        return "File not found on server", 404

    try:
        # 1. Initialize the cipher with the provided key
        cipher_suite = Fernet(key.encode('utf-8'))
        
        # 2. Read the encrypted file
        with open(enc_filepath, 'rb') as f:
            encrypted_data = f.read()

        # 3. Decrypt the data
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        
        # 4. Save the decrypted file temporarily to serve it
        dec_filename = "decrypted_" + filename.replace('.enc', '')
        dec_filepath = os.path.join(app.config['UPLOAD_FOLDER'], dec_filename)

        with open(dec_filepath, 'wb') as f:
            f.write(decrypted_data)

        # 5. Send file back to user
        return send_file(dec_filepath, as_attachment=True)
    
    except Exception as e:
        return f"<h2>Decryption Failed!</h2><p>Invalid Key or Corrupted File.</p>", 400

if __name__ == '__main__':
    app.run(debug=True)