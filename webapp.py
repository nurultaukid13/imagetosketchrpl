from flask import Flask, request, render_template, flash, redirect, url_for
from imageToSketchConverterFacade import ImageToSketchConverterFacade
from image import Image
from color import Color

class WebApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'kelompok3rpl'
        self.facade = ImageToSketchConverterFacade()

    def run(self):
        self._setup_routes()
        self.app.run(debug=True, port=5004)

    def _setup_routes(self):
        warna = Color()
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
                    request.files['upload'].save(gambar.get_file_path())
                    gambar.set_weight()
                    return redirect(url_for('uploaded_sketch'))
                else:
                    return redirect(request.url)

        @self.app.route('/uploaded_sketch')
        def uploaded_sketch():
            if not gambar.get_file_path():
                flash('File tidak ditemukan')
                return redirect(url_for('upload_page'))
            else:
                sketch_image = self.facade.convert_to_sketch(gambar.get_file_path(), 'static/sketch')
                return render_template('upload.html', file_path = sketch_image)
            
        @self.app.route('/uploaded_sketch/coloring', methods=['POST'])
        def proces_color():
            warna.set_rgb_color(request.form.get('color'))
            return redirect(url_for('color_page'))
        
        @self.app.route('/uploaded_coloring')
        def color_page():
            colorsketch=warna.hex_to_rgb(warna.get_rgb_color())
            self.facade.set_color(self.facade.get_sketch_image(), colorsketch)
            return render_template('upload.html', color=colorsketch, file_path=self.facade.get_coloring_image())
            
        @self.app.route('/download', methods=['GET'])
        def download_file():
            compress_checkbox = request.args.get('compress') == 'on'
    
            if compress_checkbox:
                if self.facade.get_coloring_image():
                    compressed_sketch = self.facade.compress_image(self.facade.get_coloring_image(), max_size=1920)  # Adjust the `max_size` as needed
                else:
                    compressed_sketch = self.facade.compress_image(self.facade.get_sketch_image(), max_size=1920)  # Adjust the `max_size` as needed
                return self.facade.download_sketch()
            else:
                return self.facade.download_sketch()


if __name__ == "__main__":
    web_app = WebApp()
    web_app.run()