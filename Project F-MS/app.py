import os
import time
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def loading_screen():
    return render_template('index.html')

@app.route('/Database', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
   
        if 'file' not in request.files:
            return render_template('database.html', error='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('database.html', error='No selected file')

        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        upload_folder = os.path.join(desktop_path, 'uploads', datetime.now().strftime('%Y%m%d%H%M%S'))

        os.makedirs(upload_folder, exist_ok=True)
        file.save(os.path.join(upload_folder, file.filename))
        return render_template('database.html', success='File uploaded successfully')

    return render_template('database.html')

@app.route('/OS')
def file_explorer():
    return render_template('os.html')

@app.route('/select_file', methods=['POST'])
def select_file():
    selected_file = None
    if 'file' in request.files:
        file = request.files['file']
        file_info = {
            'name': file.filename,
            'size': len(file.read()),
            'extension': file.filename.split('.')[-1].lower()
        }

        if file_info['extension'] == 'pdf':
            selected_file = {
                'info': file_info,
                'is_pdf': True
            }
        else:
            selected_file = {
                'info': file_info,
                'is_pdf': False
            }

    return render_template('os.html', selected_file=selected_file)

@app.route('/Files')
def settings():
    return render_template('files.html')

if __name__ == '__main__':
    app.run(debug=True)