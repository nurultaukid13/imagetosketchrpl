import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, redirect, request, url_for, session, flash
from imageToSketchConverter import ImageToSketchConverter

app = Flask(__name__)
app.secret_key = 'kelompok3rpl'
sketch=ImageToSketchConverter()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/upload/sketch', methods=['POST'])
def upload_sketch():
    if 'upload' not in request.files:
        flash('File tidak ditemukan')
        return redirect(request.url)

    file = request.files['upload']
    if file.filename == '':
        flash('File belum dipilih')
        return redirect(request.url)

    filename = secure_filename(file.filename)
    if not allowed_file(filename):
        flash('Tipe file tidak diizinkan')
        return redirect(request.url)

    file_path = os.path.join('static/original', filename)
    file.save(file_path)

    session['file_path'] = file_path
    flash('File berhasil diupload')
    return redirect(url_for('uploaded_sketch'))

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in {'png', 'jpg', 'jpeg'}

@app.route('/uploaded_sketch')
def uploaded_sketch():
    file_path = session.get('file_path', None)
    if not file_path:
        flash('File tidak ditemukan')
        return redirect(url_for('upload_page'))
    else:
        sketch.convert_to_sketch(file_path, 'static/sketch')
        session['sketch'] = sketch.sketch_image
    return render_template('upload.html', file_path=sketch.sketch_image)

@app.route('/download', methods=['GET'])
def download_file():
    return sketch.download_sketch()

if __name__ == '__main__':
    app.run(debug=True, port=5002)