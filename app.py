from flask import Flask, request, send_file, render_template, jsonify
import os
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        with open(file_path, 'rb') as f:
            response = requests.post('https://file.io', files={'file': f})
            if response.status_code == 200:
                data = response.json()
                return jsonify({'key': data['key'], 'filename': file.filename}), 200
            else:
                return 'Failed to upload file', 500

@app.route('/download/<key>', methods=['GET'])
def download_file(key):
    file_link = f'https://file.io/{key}'
    response = requests.get(file_link)
    if response.status_code == 200:
        temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], key)
        with open(temp_file_path, 'wb') as f:
            f.write(response.content)
        
        filename = key.split('/')[-1]
        return send_file(temp_file_path, as_attachment=True, download_name=filename)
    else:
        return 'Failed to download file', 500

if __name__ == '__main__':
    app.run(debug=True)
