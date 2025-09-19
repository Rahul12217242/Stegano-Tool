import os
from flask import Flask, request, render_template, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename
from stegano import lsb

# --- Configuration ---
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'bmp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'a_secret_key_for_flash_messages'

# Ensure the upload directory exists when the app starts
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Helper Function ---
def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Main Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    """Handles the main page logic for both encoding and decoding."""
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['image']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # --- ENCODE LOGIC ---
            if 'encode' in request.form:
                secret_message = request.form['secret']
                if not secret_message:
                    flash('Secret message cannot be empty for encoding.')
                    return redirect(request.url)
                
                try:
                    encoded_image = lsb.hide(filepath, secret_message)
                    encoded_filename = 'encoded_' + filename
                    encoded_filepath = os.path.join(app.config['UPLOAD_FOLDER'], encoded_filename)
                    encoded_image.save(encoded_filepath)
                    return render_template('result.html', encoded=True, image_name=encoded_filename)
                except Exception as e:
                    flash('Encoding failed. The secret message may be too long for this image.')
                    return redirect(request.url)

            # --- DECODE LOGIC ---
            elif 'decode' in request.form:
                try:
                    secret_message = lsb.reveal(filepath)
                    if not secret_message:
                        secret_message = "No hidden message found in this image."
                except Exception as e:
                    secret_message = f"An error occurred. Is this an encoded image?"
                
                return render_template('result.html', decoded=True, message=secret_message)
        else:
            flash('Invalid file type. Please upload a PNG or BMP file.')
            return redirect(request.url)

    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Provides a route to download the encoded image."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
