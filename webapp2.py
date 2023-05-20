from flask import Flask, request, render_template, flash, redirect, url_for
from imageToSketchConverter import ImageToSketchConverter
from image import Image

class WebApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'kelompok3rpl'
        
    # def __init__(self, facade: ImageToSketchConverterFacade):
    #     self.app = Flask(__name__)
    #     self.facade = facade

    def run(self):
        self._setup_routes()
        self.app.run(debug=True, port=5002)

    def _setup_routes(self):
        gambar = Image()
        sketch = ImageToSketchConverter()

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
                sketch.convert_to_sketch(gambar.file_path, 'static/sketch')
                return render_template('upload.html', file_path = sketch.sketch_image)

        @self.app.route('/download', methods=['GET'])
        def download_file():
            return sketch.download_sketch()

    # @self.app.route("/convert", methods=["POST"])
    # def convert_to_sketch():
    #     image_path = request.form.get("image_path")
    #     color_hex_code = request.form.get("color_hex_code")

    #     if not image_path or not color_hex_code:
    #         return jsonify({"error": "Missing required parameters"}), 400

    #     compressed_sketch = self.facade.convert_to_sketch(image_path, color_hex_code)
    #     return jsonify({"compressed_sketch": compressed_sketch})

    # @self.app.route("/compress", methods=["POST"])
    # def compress_sketch():
    #     # Implement the logic to compress the sketch image
    #     # and return the path of the compressed sketch image file
    #     pass

    # @self.app.route("/download", methods=["POST"])
    # def download_sketch():
    #     # Implement the logic to download the sketch image
    #     # Return the path of the downloaded sketch image file
    #     pass


if __name__ == "__main__":
    # facade = ImageToSketchConverterFacade()
    # web_app = WebApp(facade)
    web_app = WebApp()
    web_app.run()