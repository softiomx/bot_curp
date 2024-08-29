from flask import Flask, send_file,request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import random
from selenium.webdriver.common.by import By

app = Flask(__name__)

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    # Obtener el CURP del cuerpo de la solicitud
    data = request.get_json()
    curp = data.get('curp')

    if not curp:
        return jsonify({"error": "CURP es requerido"}), 400

    # Configura la ruta base para las descargas
    base_download_dir = ""
    user_download_dir = os.path.join(base_download_dir, curp)

    # Crear la carpeta de descargas para el usuario si no existe
    os.makedirs(user_download_dir, exist_ok=True)

    # Configura las opciones del navegador
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36")
    chrome_options.add_argument("--disable-webrtc")

    # Configurar las preferencias de descarga directamente en las opciones
    chrome_options.add_argument(f"download.default_directory={user_download_dir}")
    chrome_options.add_argument("download.prompt_for_download=false")
    chrome_options.add_argument("download.directory_upgrade=true")
    chrome_options.add_argument("plugins.always_open_pdf_externally=true")

    # Inicializar el servicio de ChromeDriver
    service = Service(ChromeDriverManager().install())

    # Inicializar el navegador usando Selenium estándar
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Eliminar la propiedad "webdriver" para evitar detección
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Abre la página web
        driver.get('https://www.gob.mx/curp/')

        # Espera un tiempo aleatorio para simular comportamiento humano
        time.sleep(random.uniform(2, 5))

        # Encuentra el campo de entrada de CURP
        curp_input = driver.find_element(By.ID, 'curpinput')
        curp_input.send_keys(curp)

        # Espera otro tiempo aleatorio antes de realizar la siguiente acción
        time.sleep(random.uniform(2, 5))

        # Encuentra y haz clic en el botón de búsqueda
        buscar_button = driver.find_element(By.ID, 'searchButton')
        buscar_button.click()

        # Espera a que el PDF se genere y se muestre
        time.sleep(random.uniform(5, 10))

        # Encuentra el enlace o botón que genera el PDF y haz clic en él
        pdf_button = driver.find_element(By.ID, 'download')
        pdf_button.click()

        # Espera la descarga del archivo PDF
        time.sleep(random.uniform(5, 10))

    finally:
        # Cierra el navegador
        driver.quit()

    # Verifica si el archivo PDF fue descargado
    files = os.listdir("/Users/jdionicio/Downloads")
    pdf_files = [file for file in files if file.endswith(".pdf") and file.startswith(f"CURP_{curp}")]
    if pdf_files:
        pdf_file = pdf_files[0]
        file_path = os.path.join("/Users/jdionicio/Downloads", pdf_file)
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "No se encontró el archivo PDF."}), 404


if __name__ == '__main__':
    app.run(debug=True)
