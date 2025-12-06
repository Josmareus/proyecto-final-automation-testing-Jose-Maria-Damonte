from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def is_element_present(driver, by, value, timeout=10):
    """
    Verifica si un elemento está presente en la página.
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return True
    except TimeoutException:
        return False

def is_element_visible(driver, by, value, timeout=10):
    """
    Verifica si un elemento está visible en la página.
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        return True
    except TimeoutException:
        return False

def perform_login(driver, username, password):
    """
    Login en el sitio SauceDemo.
    """
    from selenium.webdriver.common.by import By
    
    driver.get("https://www.saucedemo.com/")
    
    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    
    username_input.send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    
    driver.find_element(By.ID, "login-button").click()
    
    WebDriverWait(driver, 10).until(
        EC.url_contains("inventory.html")
    )

def add_product_to_cart(driver, product_index=0):
    """
    Añade un producto específico al carrito.
    En caso de no indicar el índice, será el primer producto.
    """
    from selenium.webdriver.common.by import By
    
    products = driver.find_elements(By.CLASS_NAME, "inventory_item")
    
    if product_index >= len(products):
        raise IndexError(f"Índice de producto {product_index} fuera de rango (hay {len(products)} productos)")
    
    product = products[product_index]
    
    product_name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
    
    add_button = product.find_element(By.XPATH, ".//button[contains(@data-test, 'add-to-cart')]")
    add_button.click()
    
    return product_name

def get_cart_count(driver):
    """
    Obtiene el número de productos en la sección del Carrito.
    """
    from selenium.webdriver.common.by import By
    
    try:
        badge = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        return int(badge.text)
    except TimeoutException:
        return 0

def take_screenshot(driver, filename):
    """
    Toma una captura de pantalla y la guarda con el nombre provisto.
    """
    try:
        driver.save_screenshot(f"screenshots/{filename}")
        print(f"Captura de pantalla guardada: {filename}")
    except Exception as e:
        print(f"Error al guardar la captura de pantalla: {e}")