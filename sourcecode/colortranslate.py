
def hex_to_rgba(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
    return (r / 255.0, g / 255.0, b / 255.0)
