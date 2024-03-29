import numpy as np
import imageio
import scipy.ndimage
import cv2
import os
from flask import send_file
from PIL import Image

class ImageToSketchConverter:
    def __init__(self):
        self.original_image = ""
        self.sketch_image = ""
        self.compressed_image = ""
        self.coloring_image=""
    
    def get_compressed_image(self)->str:
        return self.compressed_image
    
    def get_coloring_image(self)->str:
        return self.coloring_image
    
    def get_sketch_image(self):
        return self.sketch_image
    
    #konversi image to sketch
    @staticmethod
    def dodge(front,back):
        result=front*255/(255-back)
        result[result>255]=255
        result[result==255]=255
        return result.astype("uint8")
        
    @staticmethod
    def grayscale(rgb):
        return np.dot(rgb[...,:3],[0.299,0.587,0.114])
        
    def convert_to_sketch(self, original: str, sketch_location: str)->str:
        self.original_image = original
        sketch_location

        img = imageio.imread(self.original_image)
        g = self.grayscale(img)
        i = 255 - g
        b = scipy.ndimage.filters.gaussian_filter(i, sigma=10)
        hasil_sketch = self.dodge(b, g)
        self.sketch_image = f"{sketch_location}/{os.path.basename(self.original_image)}"
        
        hasil_sketch = cv2.cvtColor(hasil_sketch, cv2.COLOR_BGR2RGB)
        
        cv2.imwrite(self.sketch_image, hasil_sketch)
        return self.sketch_image
    
    # mengubah warna sketch
    def coloring(self, sketch_image: str, rgb_color: str) -> str:
        gambar_tnpa_putih = self.blend_if_gray(sketch_image, 243)
        colored_image = self.color_overlay(gambar_tnpa_putih, rgb_color)
        colored_image_rgb = colored_image.convert("RGB")  # Convert to RGB mode
        # Ambil format gambar dari sketch_image tanpa titik
        image_format = os.path.splitext(sketch_image)[1][1:].lower()
        if image_format == 'PNG':
            format_image = 'PNG'
        else:
            format_image ='JPEG'
        basename = os.path.basename(sketch_image)
        self.coloring_image = os.path.join("static", "coloring", basename)
        # Simpan gambar dengan format yang sesuai
        colored_image_rgb.save(self.coloring_image, format=format_image)
        return self.coloring_image

    #menghilangkan warna putih pada gambar
    @staticmethod
    def blend_if_gray(gambar_path, ambang):
        img = Image.open(gambar_path).convert("RGBA")
        data = img.getdata()

        new_data = []
        for item in data:
            # Ambil nilai rata-rata komponen RGB
            r, g, b, a = item
            gray_value = int((r + g + b) / 3)

            # Jika nilai rata-rata lebih besar dari ambang, set transparansi piksel menjadi 0
            if gray_value > ambang:
                new_data.append((r, g, b, 0))
            else:
                new_data.append(item)

        img.putdata(new_data)

        # Buat objek gambar yang sudah diubah tanpa menyimpannya ke folder
        new_img = img.copy()
        return new_img
    
    #mengubah warna keseluruhan gambar
    @staticmethod
    def color_overlay(image, color):
        img = image.convert("RGBA")
        data = img.getdata()

        new_data = []
        for item in data:
            r, g, b, a = item

            new_r = (r * (255 - a) + color[0] * a) // 255
            new_g = (g * (255 - a) + color[1] * a) // 255
            new_b = (b * (255 - a) + color[2] * a) // 255

            new_data.append((new_r, new_g, new_b, a))

        img.putdata(new_data)

        return img
    
    # compress sketch image
    def compress_image(self, sketch_image: str, max_size: int, kualitas: int) -> str:
        img = Image.open(sketch_image)
        img.thumbnail((max_size, max_size))
        basename = os.path.basename(sketch_image)
        self.compressed_image = os.path.join("static", "compressed", basename)
        image_format = img.format
        img.save(self.compressed_image, format=image_format, quality=kualitas)
        return self.compressed_image
    
    # fungsi download
    def download_sketch(self, file_download):
        sketh_path = os.path.splitext(os.path.basename(file_download))
        return send_file(file_download, download_name=sketh_path[0] + '_sketch' + sketh_path[1], as_attachment=True)
