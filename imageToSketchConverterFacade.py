from imageToSketchConverter import ImageToSketchConverter

class ImageToSketchConverterFacade:
    def __init__(self):
        self.converter = ImageToSketchConverter()
        
    def get_sketch_image(self):
        sketch_location_path = self.converter.get_sketch_image()
        return sketch_location_path
    
    def get_coloring_image(self):
        coloring = self.converter.get_coloring_image()
        return coloring

    def convert_to_sketch(self, image_path: str, sketch_location: str) -> str:
        sketch_image = self.converter.convert_to_sketch(image_path, sketch_location)
        return sketch_image

    def set_color(self, sketch_image: str, rgb_color: str) -> str:
        coloring = self.converter.coloring(sketch_image, rgb_color)
        return coloring

    def compress_image(self, sketch_image: str, max_size: int, kualitas:int) -> str:
        compressing = self.converter.compress_image(sketch_image, max_size, kualitas)
        return compressing

    def download_sketch(self, file_download) -> str:
        sketch_file_path = self.converter.download_sketch(file_download)
        return sketch_file_path