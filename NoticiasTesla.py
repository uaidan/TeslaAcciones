from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
import os
import re


def noticia(url, driver):
    driver.get(url)
    sleep(2)
    driver.refresh()
    sleep(2)

    try:
        titulo_noticia = driver.find_element(By.CSS_SELECTOR, '[class^="articleHeader"]')
        sleep(2)
        titular = titulo_noticia.text.strip()  # Obtén el nombre y quita espacios en blanco
        patron = r'[a-zA-Z0-9]+\s'
        tit = re.findall(patron, titular)

        cadena = ''.join(tit)

        nombre_archivo = f"{cadena}.txt"
        archivo = 'entrenamiento/nuevas/' + nombre_archivo

        noticia_ubi = driver.find_element(By.CSS_SELECTOR, '[class^="WYSIWYG articlePage"]')
        sleep(2)
        noticia = noticia_ubi.text.strip()  # Obtén el nombre y quita espacios en blanco

        if not os.path.exists(archivo):
            with open(archivo, 'w', encoding='utf-8') as archivo_txt:
                archivo_txt.write(noticia)
            sleep(4)
        else:
            print("ya exixte este archivo")
            #sys.exit() #solo si queremos que pare el programa
    except NoSuchElementException:
        print("noticia no accesible")


def links():
    for i in range(1, 3):

        url = f"https://www.investing.com/equities/tesla-motors-news/{i}"

        driver = webdriver.Chrome()
        driver.get(url)

        sleep(2)

        try:
            captcah = driver.find_element("xpath", '//*[@id="onetrust-accept-btn-handler"]')
            captcah.click()
        except NoSuchElementException:
            print("No captcha")

        sleep(2)
        elemento = driver.find_element(By.CSS_SELECTOR, '[class^="whitespace-nowrap"]')
        driver.execute_script("arguments[0].scrollIntoView();", elemento)

        sleep(2)

        enlaces = driver.find_elements(By.CSS_SELECTOR, '[class^="inline-block text-sm leading-5 sm:text-base sm:leading-6 md:text-lg md:leading-7 font-bold mb-2 hover:underline"]')
        sleep(2)

        # Inicializa una lista para almacenar los URLs
        urls = []

        for enlace in enlaces:
            url = enlace.get_attribute('href')
            if url:
                urls.append(url)

        for url in urls:
            print(url)
            noticia(url, driver)

        driver.quit()


def menuNoticias():
    carpeta = 'entrenamiento/nuevas/'
    for archivo in os.listdir(carpeta):
        ruta_archivo = os.path.join(carpeta, archivo)
        if os.path.isfile(ruta_archivo):
            os.remove(ruta_archivo)
    links()


if __name__ == "__main__":
    menuNoticias()
