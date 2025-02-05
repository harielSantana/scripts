import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

from src.integrations.CaptchaAutomation import CaptchaAutomation

load_dotenv()

if __name__ == "__main__":
    API_KEY = os.getenv("CAPMONSTER_API_KEY")
    CAPTCHA_PAGE_URL = os.getenv("CAPTCHA_PAGE_URL")
    CHAVE_NFE = os.getenv("CHAVE_NFE")  # Adicione a chave da NF-e no .env

    if not API_KEY or not CAPTCHA_PAGE_URL or not CHAVE_NFE:
        raise ValueError("As variáveis CAPMONSTER_API_KEY, CAPTCHA_PAGE_URL e CHAVE_NFE devem estar definidas!")

    # Inicializar automação do CAPTCHA
    captcha_automation = CaptchaAutomation(CAPTCHA_PAGE_URL)
    captcha_text = captcha_automation.get_captcha_text()
    
    print(f"🔹 Texto do CAPTCHA resolvido: {captcha_text}")

    # Preencher o formulário e enviar
    driver = captcha_automation.driver  # Reaproveitar o WebDriver da automação
    time.sleep(2)  # Espera para garantir que os elementos carreguem

    try:
        # Preencher a chave da NF-e
        input_chave = driver.find_element(By.ID, "edit-txchave")  # Ajuste conforme necessário
        input_chave.send_keys(CHAVE_NFE)

        # Preencher o campo do CAPTCHA
        input_captcha = driver.find_element(By.ID, "edit-captcha-response")  # Ajuste conforme necessário
        input_captcha.send_keys(captcha_text)

        # Pressionar Enter para enviar
        input_captcha.send_keys(Keys.RETURN)
    except Exception as e:
        print(f"❌ Erro ao preencher o formulário: {e}")
        captcha_automation.close()
        exit()

    time.sleep(5)  # Espera para visualização do resultado
    
    # Verificar se uma nova aba foi aberta (indicativo de erro)
    abas = driver.window_handles
    if len(abas) > 1:
        driver.switch_to.window(abas[1])  # Mudar para a nova aba
        time.sleep(2)

        erro_mensagem = driver.find_element(By.XPATH, "/html/body/div[1]/div/header/div/div/div/div/div/div[2]/div/div/h2").text

        # Capturar mensagem de erro específica
        print(f"❌ Erro ao capturar a mensagem de erro: {erro_mensagem}")

        driver.close()  # Fechar a aba de erro
        driver.switch_to.window(abas[0])  # Voltar para a aba principal

    else:
        try:
            # Capturar resultado da pesquisa
            resultado = driver.find_element(By.ID, "resultadoNF")  # Ajuste o ID conforme necessário
            print(f"📌 Resultado da NF-e: {resultado.text}")
        except Exception as e:
            print(f"❌ Erro ao capturar o resultado: {e}")

    # Fechar navegador
    captcha_automation.close()
