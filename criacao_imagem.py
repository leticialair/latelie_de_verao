import os
import pandas as pd
import requests
from class_mail import Mail
from PIL import Image, ImageDraw, ImageFont
from unidecode import unidecode

email = "contato@lalivro.com"
senha = ""

conexao = Mail(
    "smtp.gmail.com",
    # "smtp.office365.com",
    587,
    email,
    senha,
)


class ImageCreation:

    def __init__(self):
        pass

    def get_background(self, path: str = "imagem_base_1.jpeg") -> Image.Image:
        return Image.open(path).convert("RGBA")  # Ensure it's in RGBA mode

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

    def get_font(self, font_path: str, font_size: int) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(font_path, font_size)

    def insert_title(
        self,
        background: Image.Image,
        position: tuple,
        text: str,
        font: ImageFont.FreeTypeFont,
    ) -> Image.Image:
        draw = ImageDraw.Draw(background)
        draw.text(
            position, text, font=font, fill="white"
        )  # You can adjust the fill color
        return background

    def save(
        self,
        background: Image.Image,
        name: str = "imagem_final.png",
        format: str = "PNG",
    ) -> None:
        background.save(name, format=format)
        return

    def insert_text(
        self,
        image: Image.Image,
        text: str,
        position: tuple,
        font: ImageFont.FreeTypeFont,
        color=(255, 255, 255),
    ):
        draw = ImageDraw.Draw(image)
        draw.text(position, text, font=font, fill=color)
        return image


if __name__ == "__main__":
    # Sem inserção de stickers
    # Load the Excel file
    alunos = pd.read_excel("alunos.xlsx")

    # Removendo acentos e caracteres especiais
    alunos["Nome completo\n"] = alunos["Nome completo\n"].apply(lambda x: unidecode(x))
    alunos["Nome para o Cartão de Conquistas"] = alunos[
        "Nome para o Cartão de Conquistas"
    ].apply(lambda x: unidecode(x))

    # Convert "open" links to "uc" links for direct download
    alunos["Foto para o Cartão de Conquistas"] = alunos[
        "Foto para o Cartão de Conquistas"
    ].str.replace("open", "uc")
    alunos["Foto para o Cartão de Conquistas"] = (
        alunos["Foto para o Cartão de Conquistas"] + "&export=download"
    )

    # Create output folder if it doesn't exist
    output_folder = "output_images"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each student
    for email in alunos["E-mail"].unique():
        try:
            nome = alunos[alunos["E-mail"] == email][
                "Nome para o Cartão de Conquistas"
            ].values[0]
            nome_completo = alunos[alunos["E-mail"] == email]["Nome completo\n"].values[
                0
            ]
            nome_completo = (
                nome_completo.split(" ")[0] + " " + nome_completo.split(" ")[-1]
            )
            foto = alunos[alunos["E-mail"] == email][
                "Foto para o Cartão de Conquistas"
            ].values[0]
            contagem = alunos[alunos["E-mail"] == email][
                "Contagem de palavras "
            ].values[0]

            # Download the photo
            response = requests.get(foto)
            if response.status_code == 200:
                with open("downloaded_image.png", "wb") as file:
                    file.write(response.content)

            # Open and process the image
            image = Image.open("downloaded_image.png").convert("RGBA")

            # Resize the image to the target size
            size = (300, 300)
            image = image.resize(size, Image.Resampling.LANCZOS)

            # Create a circular mask
            mask = Image.new("L", size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size[0], size[1]), fill=255)

            # Create a new RGBA image for the circular crop
            circular_image = Image.new("RGBA", size)
            circular_image.paste(image, (0, 0), mask=mask)

            # Get background
            background = ImageCreation().get_background()

            # Paste the circular image onto the background
            background.paste(circular_image, (20, 80), circular_image)

            # Set font
            font_path = (
                r"Recoleta-RegularDEMO.otf"  # Replace with the correct path to the font
            )
            font_size = 60  # Adjust the size as needed
            font = ImageFont.truetype(font_path, font_size)

            # Calculate text width and position for the name (top-right)
            draw = ImageDraw.Draw(background)
            bbox = draw.textbbox((0, 0), nome, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = background.width - text_width - 20  # Top-right position
            text_y = 120  # Lower position for the name text
            background = ImageCreation().insert_text(
                background, nome, (text_x, text_y), font
            )

            # Insert additional texts below the name
            text_1 = "0 palavras escritas"
            # text_2 = "Desafio iniciado"

            # Adjust font size for the additional texts
            font_size_small = 40
            font_small = ImageCreation().get_font(font_path, font_size_small)

            # Calculate positions for the additional texts
            text_1_bbox = draw.textbbox((0, 0), text_1, font=font_small)
            # text_2_bbox = draw.textbbox((0, 0), text_2, font=font_small)

            text_1_width = text_1_bbox[2] - text_1_bbox[0]
            # text_2_width = text_2_bbox[2] - text_2_bbox[0]

            # Insert additional text below the name
            background = ImageCreation().insert_text(
                background,
                text_1,
                (background.width - text_1_width - 20, text_y + 70),
                font_small,
            )
            # background = ImageCreation().insert_text(
            #     background,
            #     text_2,
            #     (background.width - text_2_width - 20, text_y + 110),
            #     font_small,
            # )

            # Convert the image to RGB mode before saving as JPEG
            background = background.convert("RGB")

            # Save the final image
            output_path = os.path.join(output_folder, f"{nome}.jpeg")
            background.save(output_path, format="JPEG")
            print(f"Image saved for {nome}: {output_path}")

            # Send mail
            html = f"""
            <p>
                {nome_completo},
                <br>
                <br>
                    Segue seu card do Lateliê do dia 02/12/2024!
                <br>
                    Caso publique no seu story, não esqueça de nos marcar (@lalivro)!
                <br>
                <br>
                    Atenciosamente,
                <br>
                    Equipe Lateliê
            </p>
            """

            conexao.send(
                subject=f"Card Lateliê - 02/12/2024",
                html=html,
                email="larissabr@gmail.com",
                cc="anajspacheco@gmail.com, leticia.rodrigues@investsmart.com.br",
                caminho=rf"output_images/{nome}.jpeg",
                filename=rf"output_images/{nome}.jpeg",
            )

        except Exception as err:
            print(err)

    ############################
    # Com inserção de stickers
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
