import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.aux_helpers import is_element_present, perform_login


@pytest.fixture
def driver():
    """
    Fixture que configura la instancia de Chrome WebDriver proporcionada.
    """
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Para evitar la alerta de contraseña expuesta...
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    }
    options.add_experimental_option("prefs", prefs)

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()


def test_login_success(driver):
    """
    Caso de prueba: Login exitoso con datos de acceso válidos.
    Verifica que el usuario puede acceder con su usario y contraseña y es redirigido a la página del inventario.
    """
    driver.get("https://www.saucedemo.com/")
    
    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    
    username_input.send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    
    driver.find_element(By.ID, "login-button").click()
    
    WebDriverWait(driver, 10).until(
        EC.url_contains("inventory.html")
    )
    
    assert "inventory.html" in driver.current_url, "No se redirigió a la página de inventario"
    
    print("Exitoso, login exitoso completado...!")


def test_login_fail(driver):
    """
    Caso de prueba: Login con credenciales inválidas.
    Verifica que se muestra el mensaje de error.
    """
    driver.get("https://www.saucedemo.com/")

    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )

    username_input.send_keys("invalid_user")
    driver.find_element(By.ID, "password").send_keys("invalid_password")

    driver.find_element(By.ID, "login-button").click()

    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )
    
    assert "Username and password do not match" in error_message.text, "El mensaje de error no es el esperado"
    print("Exitoso, prueba de credenciales inválidas completada...!")


def test_verify_catalog(driver):
    """
    Caso de prueba: Verificación de la lista de productos.
    Comprueba que el título de la página sea el correcto, que existan productos listados 
    y que los elementos importantes de la interfaz estén presentes en la página.
    """
    perform_login(driver, "standard_user", "secret_sauce")
    
    assert driver.title == "Swag Labs", f"El título de la página es incorrecto: {driver.title}"
    
    products = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )
    assert len(products) > 0, "Sin productos visibles en la página"
    print(f"Exitoso, se encontraron {len(products)} productos en el catálogo...!")
    
    assert is_element_present(driver, By.CLASS_NAME, "product_sort_container"), "Filtro de productos no encontrado"
    assert is_element_present(driver, By.ID, "react-burger-menu-btn"), "Menú hamburguesa no encontrado"
    assert is_element_present(driver, By.CLASS_NAME, "shopping_cart_link"), "Ícono del carrito no encontrado"
    
    print("Exitoso, verificación del catálogo completada...!")


def test_verify_cart(driver):
    """
    Caso de prueba: Interacción con productos y carrito.
    Añade un producto al carrito, verifica que el contador se incremente,
    navega al carrito y comprueba que el producto añadido esté presente.
    """
    perform_login(driver, "standard_user", "secret_sauce")
    
    assert not is_element_present(driver, By.CLASS_NAME, "shopping_cart_badge", timeout=1), "El carrito debería estar vacío inicialmente"

    product_name_element = driver.find_element(By.CLASS_NAME, "inventory_item_name")
    product_name = product_name_element.text
    print(f"Producto seleccionado: {product_name}")
    
    add_button = driver.find_element(By.XPATH, "//button[contains(@data-test, 'add-to-cart')]")
    add_button.click()
    
    cart_badge = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    assert cart_badge.text == "1", f"El contador del carrito debería ser 1, pero es {cart_badge.text}"
    print("Exitoso, producto añadido correctamente al carrito...!")
    
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    WebDriverWait(driver, 10).until(
        EC.url_contains("cart.html")
    )
    
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(cart_items) == 1, f"Debería haber 1 producto en el carrito, pero hay {len(cart_items)}"
    
    cart_item_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    assert cart_item_name == product_name, f"El producto en el carrito ({cart_item_name}) no coincide con el añadido ({product_name})"
    
    print("Exitoso, verificación del carrito completada...!")


def test_logout(driver):
    """
    Caso de prueba: Cierre de sesión.
    Verifica que el usuario pueda cerrar sesión correctamente.
    """
    perform_login(driver, "standard_user", "secret_sauce")

    driver.find_element(By.ID, "react-burger-menu-btn").click()

    logout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
    )
    
    logout_link.click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "login-button"))
    )
    
    assert driver.current_url == "https://www.saucedemo.com/", "No se redirigió a la página de login después de cerrar sesión"
    print("Exitoso, cierre de sesión completado...!")