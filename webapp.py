from flask import Flask, request, render_template, flash, redirect, url_for
from imageToSketchConverterFacade import ImageToSketchConverterFacade
from image import Image

class WebApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'kelompok3rpl'
        self.facade = ImageToSketchConverterFacade()

    def run(self):
        self._setup_routes()
        self.app.run(debug=True, port=5002)

    def _setup_routes(self):
        gambar = Image()

        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/upload')
        def upload_page():
            return render_template('upload.html')

        @self.app.route('/upload/sketch', methods=['POST'])
        def upload_sketch():
            if 'upload' not in request.files:
                flash("File tidak ditemukan")
                return redirect(request.url)
            else:
                if gambar.scan_file(request.files['upload']):
                    request.files['upload'].save(gambar.file_path)
                    return redirect(url_for('uploaded_sketch'))
                else:
                    return redirect(request.url)

        @self.app.route('/uploaded_sketch')
        def uploaded_sketch():
            if not gambar.file_path:
                flash('File tidak ditemukan')
                return redirect(url_for('upload_page'))
            else:
                sketch_image = self.facade.convert_to_sketch(gambar.file_path, 'static/sketch')
                return render_template('upload.html', file_path = sketch_image)

        @self.app.route('/download', methods=['GET'])
        def download_file():
            return self.facade.download_sketch()

if __name__ == "__main__":
    web_app = WebApp()
    web_app.run()