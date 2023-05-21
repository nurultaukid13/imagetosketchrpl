import numpy as np
import imageio
import scipy.ndimage
import cv2
import os
from flask import send_file

class ImageToSketchConverter:
    def __init__(self):
        self.original_image = ""
        self.sketch_image = ""
        self.compressed_image = ""
        self.sketch_location = ""
    
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
        self.sketch_location = sketch_location

        img = imageio.imread(self.original_image)
        g = self.grayscale(img)
        i = 255 - g
        b = scipy.ndimage.filters.gaussian_filter(i, sigma=10)
        hasil_sketch = self.dodge(b, g)
        self.sketch_image = f"{self.sketch_location}/{os.path.basename(self.original_image)}"
        
        hasil_sketch = cv2.cvtColor(hasil_sketch, cv2.COLOR_BGR2RGB)
        
        cv2.imwrite(self.sketch_image, hasil_sketch)
        return self.sketch_image
    
    # mengubah warna sketch
    def set_color(self, sketch_image:str, rgb_color: str)-> str:
        pass
    
    # compress sketch image
    def compress_image(self, sketch_image:str)->str:
        pass
    
    # fungsi download
    def download_sketch(self):
        sketh_path = os.path.splitext(os.path.basename(self.sketch_image))
        return send_file(self.sketch_image,download_name = sketh_path[0] +'_sketch' + sketh_path[1] ,as_attachment=True)