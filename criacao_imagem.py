from PIL import Image, ImageDraw, ImageFont


class ImageCreation:

    def __init__(self):
        pass

    def get_background(self, path: str = "imagem_base.png") -> Image.Image:
        return Image.open(path).convert("RGBA")

    def get_sticker(self, path: str) -> Image.Image:
        return Image.open(path).convert("RGBA")

    def paste_sticker(
        self, background: Image.Image, sticker: Image.Image, position: tuple
    ) -> None:
        background.paste(sticker, position, sticker)
        return

    def create_object(self, background: Image.Image):
        return ImageDraw.Draw(background)

    def get_font(self, path: str, size: int):
        return ImageFont.truetype(path, size)

    def insert_title(self, object, position: tuple, text, font):
        return object.text(position, text, fill="white", font=font)

    def save(
        self,
        background: Image.Image,
        name: str = "imagem_final.png",
        format: str = "PNG",
    ) -> None:
        background.save(name, format=format)
        return


if __name__ == "__main__":
    image = ImageCreation()
    background = image.get_background()
    sticker_conflito = image.get_sticker("sticker_conflito.png")
    sticker_criacao_personagem = image.get_sticker("sticker_criacao_personagem.png")
    image.paste_sticker(background, sticker_conflito, (20, 50))
    image.paste_sticker(background, sticker_criacao_personagem, (10, 70))
    object_image = image.create_object(background)
