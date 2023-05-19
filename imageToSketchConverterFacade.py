from imageToSketchConverter import ImageToSketchConverter

class ImageToSketchConverterFacade:
    def __init__(self):
        self.converter = ImageToSketchConverter()

    def convert_to_sketch(self, image_path: str, color: str):
        sketch_location = self.converter.convert_to_sketch(image_path, "sketches/")
        self.converter.set_color(sketch_location, color)
        compressed_sketch = self.converter.compress_image(sketch_location)
        return compressed_sketch

    def compress_sketch(self):
        # Implement the logic to compress the sketch image
        # Return the path of the compressed sketch image file
        pass

    def download_sketch(self, file_path: str):
        # Implement the logic to download the sketch image
        # at the specified file_path
        pass