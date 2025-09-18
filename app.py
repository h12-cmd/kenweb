from flask import Flask, render_template, request, redirect, send_from_directory, session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"  # cần để dùng session

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    my_files = session.get('my_files', [])
    return render_template('index.html', files=files, my_files=my_files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Không có file"
    file = request.files['file']
    if file.filename == '':
        return "Chưa chọn file"
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    if 'my_files' not in session:
        session['my_files'] = []
    session['my_files'].append(filename)
    session.modified = True

    return redirect('/')

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    my_files = session.get('my_files', [])
    if filename not in my_files:
        return "Bạn không được phép xóa file này"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        session['my_files'].remove(filename)
        session.modified = True
        return redirect('/')
    else:
        return "File không tồn tại"

if __name__ == '__main__':
    app.run(debug=True)