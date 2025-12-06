from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CartPage:

    def __init__(self,driver):
        self.driver = driver 
        self.wait = WebDriverWait(driver,10)

        self.carrito_items = (By.CLASS_NAME, "cart_item")
        self.nombre_items = (By.CLASS_NAME, "inventory_item_name")

    def obtener_productos_carrito(self):
        productos = self.wait.until(EC.visibility_of_all_elements_located(self.carrito_items))
        return productos
    
    def obtener_nombre_producto_carrito(self):
        nombre_producto = self.wait.until(EC.visibility_of_element_located(self.nombre_items))
        return nombre_producto.text