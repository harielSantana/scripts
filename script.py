import time
import requests
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract

# Configuração do caminho do Tesseract no Ubuntu
pytesseract.pytesseract.tesseract_cmd = "/bin/tesseract"

# Configuração do WebDriver para Chrome no Ubuntu
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Executa sem abrir a interface gráfica
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Inicia o navegador
driver = webdriver.Chrome(options=options)

# Abre a página que contém o CAPTCHA
driver.get("https://sped.fazenda.pr.gov.br/NFe/webservices/sped/nfe/completa")  # Substitua pela URL correta

# Aguarda um tempo para a página carregar
time.sleep(2)

# Localiza a imagem do CAPTCHA
captcha_element = driver.find_element(By.CSS_SELECTOR, '[data-drupal-selector="edit-captcha-image"]')

# Obtém a URL da imagem do CAPTCHA
captcha_url = captcha_element.get_attribute("src")

print("URL do CAPTCHA:", captcha_url)

# Faz o download da imagem do CAPTCHA
captcha_response = requests.get(captcha_url, stream=True)
if captcha_response.status_code == 200:
    with open("captcha.png", "wb") as f:
        f.write(captcha_response.content)
    
    # Carregar a imagem
    image = cv2.imread("captcha.png", cv2.IMREAD_GRAYSCALE)  # Converte para escala de cinza
    
    # Aplicar um filtro Gaussiano para suavizar a imagem
    image = cv2.GaussianBlur(image, (5, 5), 0)
    
    # Aplicar um threshold adaptativo
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Remover ruído usando morfologia
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    
    # Aplicar detecção de contornos para isolar caracteres
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros(image.shape, dtype=np.uint8)
    cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)
    image = cv2.bitwise_and(image, mask)
    
    # Salvar imagem processada
    cv2.imwrite("captcha_processed.png", image)
    
    # Processa a imagem com OCR
    captcha_text = pytesseract.image_to_string(Image.open("captcha_processed.png"), config="--psm 6 --oem 3")
    
    print("Captcha reconhecido:", captcha_text.strip())
else:
    print("Erro ao baixar a imagem do CAPTCHA.")

# Fecha o navegador
driver.quit()
