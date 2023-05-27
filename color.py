class Color:
    def __init__(self):
        self.rgb_color = ''    

    def set_rgb_color(self, warna_rgb):
        self.rgb_color =  warna_rgb
    
    @staticmethod
    def hex_to_rgb(hex_code):
        hex_code = hex_code.lstrip('#')
        if len(hex_code) != 6:
            # Return a default color if the hex code is invalid
            return (0, 0, 0)  # Black color
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)
        return (r, g, b)
    
    def get_rgb_color(self) -> str:
        return self.rgb_color