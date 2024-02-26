from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


def compra_venta(driver, cantidad, accion):

    wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos

    if accion == 0:
        # selecciona el campo para cambiar la opccion
        action_div = driver.find_element(By.CSS_SELECTOR, "div.v-select__selection--comma")
        driver.execute_script("arguments[0].click();", action_div)

        # selecciona la accion como venta
        sell_div = driver.find_element(By.XPATH, "//div[contains(@class, 'v-list-item__title') and text()='Sell']")
        driver.execute_script("arguments[0].click();", sell_div)

    try:
        # Localizar el campo de entrada de cantidad y enviar un número
        quantity_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-cy='quantity-input']")))
        quantity_input.send_keys(cantidad)

        # mandar orden de compra
        sleep(2)
        preview_button = driver.find_element(By.CSS_SELECTOR, "button[data-cy='preview-button']")
        driver.execute_script("arguments[0].click();", preview_button)

        # confirmar orden de compra
        sleep(2)
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[data-cy='submit-order-button']")
        driver.execute_script("arguments[0].click();", submit_button)

    except Exception as e:
        print("Error al enviar número al campo de cantidad:", e)


def login(driver):

    # mandamos nuestras credencialess
    sleep(2)
    driver.find_element("xpath", '//*[@id="username"]').send_keys("teslaacciones@gmail.com")  #Tu email
    sleep(2)
    driver.find_element("xpath", '//*[@id="password"]').send_keys("Tg.vinvp+")  #Tu contraseña

    # nos logeamos en la pagina
    sleep(2)
    driver.find_element("xpath", '//*[@id="login"]').click()

    try:
        sleep(2)
        driver.find_element("xpath", '//*[@id="login"]').click()
    except NoSuchElementException:
        prruuu = 0

    try:
        # Rechazar cookies
        sleep(2)
        driver.find_element("xpath", '//*[@id="onetrust-close-btn-container"]/button').click()
    except NoSuchElementException:
        print("Error: No se pudo encontrar el botón para rechazar cookies.")
        driver.quit()  # Cerrar el navegador

        return 0


def main_bot(cantidad, accion):
    url = "https://www.investopedia.com/simulator/trade/stocks"
    chrome_options = webdriver.ChromeOptions()

    # Inicializa el navegador Chrome con la ruta especificada a ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    # Minimiza la ventana del navegador
    #driver.minimize_window()

    estado = login(driver)
    sleep(2)


    if estado == 0:
        print("Error: no se ha podido conectar con el servidor web")
    else:
        driver.get(url)
        sleep(2)

        wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos

        try:
            # Localizar el campo de búsqueda e introduce TSLA
            search_box = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Look up Symbol/Company Name']")))
            search_box.send_keys("TSLA")

            # selecciona las acciones de TESLA
            first_option = wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'list-item-') and contains(@id, '-0')]")))
            first_option.click()

            compra_venta(driver, cantidad, accion)

            sleep(2)
        except Exception as e:
            print("Error al localizar el elemento:", e)
        finally:
            # Cerrar el navegador al final, independientemente de si el script fue exitoso o no
            driver.quit()

    return estado


if __name__ == "__main__":
    main_bot()
