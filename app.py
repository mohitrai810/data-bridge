from flask import Flask, request, send_file, render_template, redirect, url_for
import os
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    upload_result = request.args.get('upload_result')
    download_result = request.args.get('download_result')
    return render_template('index.html', upload_result=upload_result, download_result=download_result)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index', upload_result='No file part'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index', upload_result='No selected file'))
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        with open(file_path, 'rb') as f:
            response = requests.post('https://file.io', files={'file': f})
            if response.status_code == 200:
                data = response.json()
                file_key = data.get('key')
                if file_key:
                    return redirect(url_for('index', upload_result=file_key))
            return redirect(url_for('index', upload_result='Failed to upload file'))

@app.route('/download', methods=['POST'])
def download_file():
    file_key = request.form.get('fileKey')
    file_name = request.form.get('fileName')

    if not file_key or not file_name:
        return redirect(url_for('index', download_result='Please enter both code and file name'))

    file_link = f'https://file.io/{file_key}'
    response = requests.get(file_link)
    if response.status_code == 200:
        temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        with open(temp_file_path, 'wb') as f:
            f.write(response.content)

        return send_file(temp_file_path, as_attachment=True, download_name=file_name)
    else:
        return redirect(url_for('index', download_result='Failed to download file'))

if __name__ == '__main__':
    app.run(debug=True)
