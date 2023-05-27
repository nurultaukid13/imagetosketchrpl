from PIL import Image

def resize_image(input_path, output_path, max_size):
    image = Image.open(input_path)
    image.thumbnail((max_size, max_size))
    image.save(output_path)

# Contoh penggunaan
input_file = 'DSC00040.JPG'  # Ganti dengan lokasi file gambar input
output_file = 'static/compres/batman.jpg'  # Ganti dengan lokasi file hasil perubahan ukuran

max_size = 500  # Ganti dengan ukuran maksimum yang diinginkan

resize_image(input_file, output_file, max_size)
