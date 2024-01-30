import os
import time
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__, static_url_path='/static')
app.config['uploads'] = 'C:\\Users\\bibho\\Desktop\\Github\\FileManagementSystem\\Project F-MS\\static\\storage'
storage_path = app.config['uploads']

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
        upload_folder = os.path.join(desktop_path, 'storage', datetime.now().strftime('%Y%m%d%H%M%S'))

        os.makedirs(upload_folder, exist_ok=True)
        file.save(os.path.join(upload_folder, file.filename))
        return render_template('database.html', success='File uploaded successfully')

    return render_template('database.html')

@app.route('/OS')
def file_explorer():
    stored_files = os.listdir(storage_path)
    return render_template('os.html', stored_files=stored_files)

@app.route('/serve_uploaded_file/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['uploads'], filename)

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
                'is_pdf': True,
                'is_image': False
            }
        elif file_info['extension'] in ['jpg', 'jpeg', 'png', 'gif']:
            selected_file = {
                'info': file_info,
                'is_pdf': False,
                'is_image': True
            }
            file.save(os.path.join(app.config['uploads'], file_info['name']))  # Save the file

        else:
            selected_file = {
                'info': file_info,
                'is_pdf': False,
                'is_image': False
            }

    return render_template('os.html', selected_file=selected_file)

if __name__ == '__main__':
    app.run(debug=True)