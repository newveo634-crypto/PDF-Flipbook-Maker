import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for

app = Flask(__name__)

# --- CONFIGURATION FOR PYTHONANYWHERE ---
# IMPORTANT: Replace 'azizurrehman' with your actual PythonAnywhere username
USERNAME = 'aziz786'
BASE_DIR = f'/home/{USERNAME}/flipbook-maker'

# Paths for folders
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists on the server
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    # Looks for a file parameter in the URL (e.g., /?file=mybook.pdf)
    filename = request.args.get('file')
    return render_template('index.html', filename=filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return "No file part", 400
    
    file = request.files['pdf_file']
    
    if file.filename == '':
        return "No selected file", 400
    
    if file and file.filename.endswith('.pdf'):
        # Securely save the file to the uploads directory
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Redirect to show the flipbook
        return redirect(url_for('index', file=file.filename))
    
    return "Please upload a valid PDF file.", 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # This serves the file so the browser can read it
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # For local testing only
    app.run(debug=True)
