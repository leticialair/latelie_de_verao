from PIL import Image, ImageDraw, ImageFont


class ImageCreation:

    def __init__(self):
        pass

    def get_background(self, path: str = "imagem_base.png") -> Image.Image:
        return Image.open(path).convert("RGBA")

    def get_sticker(self, path: str, size: tuple = ()) -> Image.Image:
        sticker = Image.open(path).convert("RGBA")
        if len(size) > 0:
            sticker = sticker.resize(size, Image.LANCZOS)
        return sticker

    def paste_sticker(
        self, background: Image.Image, sticker: Image.Image, position: tuple
    ) -> None:
        background.paste(sticker, position, sticker)
        return

    def create_object(self, background: Image.Image) -> ImageDraw.ImageDraw:
        return ImageDraw.Draw(background)

    def get_font(self, path: str, size: int):
        return ImageFont.truetype(path, size)

    def insert_title(self, object, position: tuple, text, font):
        object.text(position, text, fill="white", font=font)
        return

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
    sticker_conflito = image.get_sticker("sticker_conflito.png", size=(432, 664))
    sticker_criacao_personagem = image.get_sticker(
        "sticker_criacao_personagem.png", size=(432, 768)
    )

    width_background, height_background = background.size
    top_left = (0, 0)
    center_sticker_conflito = (
        (width_background - sticker_conflito.width) // 2,
        (height_background - sticker_conflito.height) // 2,
    )
    bottom_right_sticker_criacao_personagem = (
        width_background - sticker_criacao_personagem.width,
        height_background - sticker_criacao_personagem.height,
    )

    image.paste_sticker(background, sticker_conflito, center_sticker_conflito)
    image.paste_sticker(
        background, sticker_criacao_personagem, bottom_right_sticker_criacao_personagem
    )
    object_image = image.create_object(background)
    font = image.get_font("04font.ttf", 80)
    text_width, _ = font.getsize("Fulano de Tal")
    image.insert_title(
        object_image, ((background.width - text_width), 10), "Fulano de Tal", font
    )
    image.save(background)
