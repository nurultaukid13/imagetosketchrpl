from flask import Flask, request, jsonify
from imageToSketchConverter import ImageToSketchConverter, Image, Color
from imageToSketchConverterFacade import ImageToSketchConverterFacade

class WebApp:
    def __init__(self, facade: ImageToSketchConverterFacade):
        self.app = Flask(__name__)
        self.facade = facade

    def run(self):
        self._setup_routes()
        self.app.run()

    def _setup_routes(self):
        @self.app.route("/convert", methods=["POST"])
        def convert_to_sketch():
            image_path = request.form.get("image_path")
            color_hex_code = request.form.get("color_hex_code")
            
            if not image_path or not color_hex_code:
                return jsonify({"error": "Missing required parameters"}), 400

            compressed_sketch = self.facade.convert_to_sketch(image_path, color_hex_code)
            return jsonify({"compressed_sketch": compressed_sketch})

        @self.app.route("/compress", methods=["POST"])
        def compress_sketch():
            # Implement the logic to compress the sketch image
            # and return the path of the compressed sketch image file
            pass

        @self.app.route("/download", methods=["POST"])
        def download_sketch():
            # Implement the logic to download the sketch image
            # Return the path of the downloaded sketch image file
            pass

if __name__ == "__main__":
    facade = ImageToSketchConverterFacade()
    web_app = WebApp(facade)
    web_app.run()
