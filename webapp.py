from flask import Flask, request, render_template, flash, redirect, url_for
from imageToSketchConverterFacade import ImageToSketchConverterFacade
from image import Image
from color import Color
from filemanager import FileManager


class WebApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'kelompok3rpl'
        self.facade = ImageToSketchConverterFacade()
        self.filemanager = FileManager()

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
                    self.filemanager.delete_files_in_folder_after_timeout('original', 60)
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
                self.filemanager.delete_files_in_folder_after_timeout('sketch', 60)
                gambar.set_file_path_before_compress(gambar.get_file_name(), 'static/sketch')
                gambar.set_weight_before_compress()
                file_weight = gambar.get_weight_before_compress()
                gambar.file_path_download = sketch_image
                return render_template('upload.html', file_path=gambar.file_path_download, file_weight=round(file_weight/1000))

        @self.app.route('/uploaded_sketch/coloring', methods=['POST'])
        def proces_color():
            warna.set_rgb_color(request.form.get('color'))
            return redirect(url_for('color_page'))

        @self.app.route('/uploaded_coloring')
        def color_page():
            colorsketch = warna.hex_to_rgb(warna.get_rgb_color())
            if colorsketch==(255,255,255):
                gambar.file_path_download = self.facade.get_sketch_image()
                gambar.set_file_path_before_compress( gambar.get_file_name(), 'static/sketch')
                gambar.set_weight_before_compress()
                file_weight = gambar.get_weight_before_compress()
                warna.set_rgb_color(colorsketch)
            else:
                self.facade.set_color(self.facade.get_sketch_image(), colorsketch)
                self.filemanager.delete_files_in_folder_after_timeout('coloring', 60)
                gambar.set_file_path_before_compress( gambar.get_file_name(), 'static/coloring')
                gambar.set_weight_before_compress()
                file_weight = gambar.get_weight_before_compress()
                gambar.file_path_download = self.facade.get_coloring_image()
            return render_template('upload.html', file_path=gambar.file_path_download, file_weight = round(file_weight/1000), color=colorsketch)
            
        @self.app.route('/download', methods=['GET'])
        def download_file():
            compress_checkbox = request.args.get('compress') == 'on'
            if compress_checkbox:
                if self.facade.get_coloring_image() and self.facade.get_coloring_image() == 'static/coloring/'+gambar.file_name and warna.get_rgb_color()!=(255,255,255):
                    gambar.file_path_download = self.facade.compress_image(self.facade.get_coloring_image(), max_size=540)
                else:
                    gambar.file_path_download = self.facade.compress_image(self.facade.get_sketch_image(), max_size=1080)
            else:
                if self.facade.get_coloring_image() and self.facade.get_coloring_image() == 'static/coloring/'+gambar.file_name and warna.get_rgb_color()!=(255,255,255):
                    gambar.file_path_download = self.facade.get_coloring_image()
                else:
                    gambar.file_path_download = self.facade.get_sketch_image()
            self.filemanager.delete_files_in_folder_after_timeout('compressed', 60)
            return self.facade.download_sketch(gambar.file_path_download)

if __name__ == "__main__":
    app = WebApp().app
    app.run()
