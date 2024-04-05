import os
import time
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory, jsonify, redirect, url_for

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
    stored_files = os.listdir(storage_path)
    return send_from_directory(app.config['uploads'], filename, stored_files=stored_files)

@app.route('/select_file', methods=['POST'])
def select_file():
    stored_files = os.listdir(storage_path)
    selected_file = None
    if 'file' in request.files:
        file = request.files['file']
        file_info = {
            'name': file.filename,
            'size': len(file.read()),
            'extension': file.filename.split('.')[-1].lower()
        }

        file.save(os.path.join(app.config['uploads'], file_info['name']))

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

        elif file_info['extension'] in ['glb', 'gltf', 'fbx', 'obj']:  
            selected_file = {
                'info': file_info,
                'is_pdf': False,
                'is_image': False,
                'is_glb': True,
                'is_gltf': True,
                'is_fbx': True,
                'is_obj': True  
            }

        else:
            selected_file = {
                'info': file_info,
                'is_pdf': False,
                'is_image': False
            }

    return render_template('os.html', selected_file=selected_file, stored_files=stored_files)

@app.route('/search_files', methods=['POST'])
def search_files():
    query = request.form.get('query')
    stored_files = os.listdir(storage_path)
    search_results = [filename for filename in stored_files if query.lower() in filename.lower()]
    return render_template('os.html', stored_files=search_results)

@app.route('/delete_file/<filename>', methods=['GET'])
def delete_file(filename):
    if os.path.exists(os.path.join(storage_path, filename)):
        os.remove(os.path.join(storage_path, filename))
        return redirect(url_for('file_explorer'))
    else:
        return jsonify({'message': 'File not found'})

if __name__ == '__main__':
    app.run(debug=True)
