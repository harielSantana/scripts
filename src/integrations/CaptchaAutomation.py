import time
import os


from selenium import webdriver
from selenium.webdriver.common.by import By

from src.integrations.CapMonster import CaptchaSolver

class CaptchaAutomation:
    def __init__(self, page_url: str):
        self.driver = self._init_webdriver()
        self.page_url = page_url

    def _init_webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)

    def get_captcha_image_url(self) -> str:
        self.driver.get(self.page_url)
        time.sleep(2)
        captcha_element = self.driver.find_element(By.CSS_SELECTOR, '[data-drupal-selector="edit-captcha-image"]')
        return captcha_element.get_attribute("src")
    
    def get_captcha_text(self) -> str:
        solver = CaptchaSolver(api_key=os.getenv("CAPMONSTER_API_KEY"))
        captcha_url = self.get_captcha_image_url()
        captcha_text = solver.process_captcha(captcha_url)
        return captcha_text


    def close(self):
        self.driver.quit()
