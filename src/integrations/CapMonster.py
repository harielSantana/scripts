import os
import asyncio
import base64
import requests

from capmonstercloudclient import CapMonsterClient, ClientOptions
from capmonstercloudclient.requests import ImageToTextRequest

class CaptchaSolver:
    def __init__(self, api_key: str, save_path="src/files"):
        self.client_options = ClientOptions(api_key=api_key)
        self.cap_monster_client = CapMonsterClient(options=self.client_options)
        self.save_path = save_path

        # Cria a pasta caso não exista
        os.makedirs(self.save_path, exist_ok=True)

    def download_captcha_image(self, url: str) -> str:
        """Baixa a imagem do CAPTCHA e a salva em um arquivo local."""
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            image_path = os.path.join(self.save_path, "captcha.jpg")

            with open(image_path, "wb") as file:
                file.write(response.content)

            print(f"✅ Imagem do CAPTCHA salva em: {image_path}")
            return image_path
        else:
            raise Exception(f"Erro ao baixar a imagem do CAPTCHA. Status: {response.status_code}")

    async def solve_captcha(self, image_path: str) -> str:
        """Lê a imagem salva e resolve o CAPTCHA."""
        with open(image_path, "rb") as file:
            image_bytes = file.read()

        image_to_text_request = ImageToTextRequest(image_bytes=image_bytes)
        return await self.cap_monster_client.solve_captcha(image_to_text_request)

    def process_captcha(self, image_url: str) -> str:
        """Executa o processo de baixar, armazenar e resolver o CAPTCHA."""
        captcha_image_path = self.download_captcha_image(image_url)

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            return loop.create_task(self.solve_captcha(captcha_image_path))
        else:
            return asyncio.run(self.solve_captcha(captcha_image_path))
