from PIL import Image

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
    img.save('coba/coba.png')

def color_overlay(gambar_path, color):
    img = Image.open(gambar_path).convert("RGBA")
    data = img.getdata()

    new_data = []
    for item in data:
        r, g, b, a = item

        # Gunakan nilai warna overlay untuk mengganti komponen RGB gambar
        new_r = (r * (255 - a) + color[0] * a) // 255
        new_g = (g * (255 - a) + color[1] * a) // 255
        new_b = (b * (255 - a) + color[2] * a) // 255

        new_data.append((new_r, new_g, new_b, a))

    img.putdata(new_data)
    img.save('coba/coba.png')

# Contoh penggunaan
gambar_path = "batman_sketch.jpeg"  # Ganti dengan path gambar yang ingin diproses
ambang = 243  # Ganti dengan ambang warna (0-255) yang ingin digunakan
color = (255, 0, 0)

blend_if_gray(gambar_path, ambang)
color_overlay('coba/coba.png', color)
