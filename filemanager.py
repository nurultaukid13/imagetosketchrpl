import os
import time

class FileManager:
    def __init__(self):
        self.static_folder = 'static'
        self.folder_names = ['original', 'sketch', 'coloring', 'compressed']
        self.folder_paths = {folder_name: os.path.join(self.static_folder, folder_name) for folder_name in self.folder_names}
        
    def delete_files_in_folder_after_timeout(self, folder_name, timeout):
        folder_path = self.folder_paths[folder_name]
        file_list = os.listdir(folder_path)
        current_time = time.time()
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and current_time - os.path.getctime(file_path) >= timeout:
                os.remove(file_path)
