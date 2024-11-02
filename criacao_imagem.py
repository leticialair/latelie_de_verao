from PIL import Image, ImageDraw, ImageFont


class Image:

    def __init__(self):
        pass

    def get_background(self, path: str = "imagem_base.png"):
        return Image.open(path).convert("RGBA")

    def get_sticker(self, path: str):
        return Image.open(path).convert("RGBA")

    def paste_sticker(self, background, sticker, position: tuple):
        return background.paste(sticker, position, sticker)

    def create_object(self, background):
        return ImageDraw.Draw(background)

    def get_font(self, path: str, size: int):
        return ImageFont.truetype(path, size)

    def insert_title(self, object, position: tuple, text, font):
        object.text(position, text, fill="white", font=font)

    def save(self, background, name: str = "imagem_final.png", format: str = "PNG"):
        background.save(name, format=format)
