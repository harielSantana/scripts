# README

## Descrição

Este script automatiza o processo de reconhecimento de CAPTCHA em uma página web. Ele utiliza Selenium para acessar a página, baixar a imagem do CAPTCHA, processá-la com OpenCV e realizar o reconhecimento de texto com Tesseract OCR.

## Requisitos

- Python 3.x
- Tesseract OCR
- Google Chrome
- ChromeDriver

## Instalação

1. Clone o repositório:
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd <NOME_DO_REPOSITORIO>
    ```

2. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

3. Instale o Tesseract OCR no Ubuntu:
    ```bash
    sudo apt-get update
    sudo apt-get install tesseract-ocr
    ```

4. Baixe e instale o ChromeDriver compatível com a versão do seu Google Chrome:
    ```bash
    wget https://chromedriver.storage.googleapis.com/<VERSAO>/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    sudo mv chromedriver /usr/local/bin/
    ```

## Uso

1. Configure o caminho do Tesseract no script:
    ```python
    pytesseract.pytesseract.tesseract_cmd = "/bin/tesseract"
    ```

2. Execute o script:
    ```bash
    python script.py
    ```

3. O script irá acessar a página, baixar a imagem do CAPTCHA, processá-la e exibir o texto reconhecido.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
