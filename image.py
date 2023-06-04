import os
from werkzeug.utils import secure_filename
from flask import flash

class Image:
    
    def __init__(self):
        self.file_name = ''
        self.file_path = ''
        self.weight = ''
        self.file_path_download = ''
        self.file_path_before_compress = ''
        self.file_weight_before_compress = ''

    def set_weight(self):
        self.weight = os.path.getsize(self.file_path)
        
    def set_file_path_before_compress(self,basename:str, folder):
        self.file_path_before_compress = os.path.join(folder, basename)
        
    def set_weight_before_compress(self):
        self.file_weight_before_compress = os.path.getsize(self.file_path_before_compress)

    def set_file_path(self,filepath:str):
        self.file_path = filepath

    def set_file_name(self,filename:str):
        self.file_name = filename
    
    @staticmethod
    def allowed_file(nama_file):
        return '.' in nama_file and \
            nama_file.rsplit('.', 1)[1] in {'png', 'jpg', 'jpeg'}
    
    def scan_file(self, request_file) -> bool:
        self.set_file_name(request_file.filename)
        if self.file_name == '':
            flash('File belum dipilih')
            return False
        else:
            securefile = secure_filename(self.file_name)
            if not self.allowed_file(self.file_name):
                flash('Tipe file tidak diizinkan')
                return False
            else:
                self.set_file_path(os.path.join('static/original', securefile))
                flash('File berhasil diupload')
                return True

    def get_file_path(self) -> str:
        return self.file_path
    
    def get_weight(self) -> int:
        return self.weight
    
    def get_file_name(self)->str:
        return self.file_name
    
    def get_weight_after_compress(self)->str:
        return self.file_weight_after_compress
        
    def get_weight_before_compress(self)->str:
        return self.file_weight_before_compress