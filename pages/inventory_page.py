from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        # Selectores de SauceDemo Inventory
        self.titulo_productos = (By.CLASS_NAME, "title")
        self.contador_carrito = (By.CLASS_NAME, "shopping_cart_badge")
        self.enlace_carrito = (By.CLASS_NAME, "shopping_cart_link")
        self.contenedor_inventario = (By.CLASS_NAME, "inventory_container")
        self.items_inventario = (By.CLASS_NAME, "inventory_item")
        self.items_inventario_nombre = (By.CLASS_NAME, "inventory_item_name")
        self.boton_agregar_carrito = (By.CSS_SELECTOR, ".inventory_item button")
    
    def obtener_todos_los_productos(self):
        self.wait.until(EC.visibility_of_all_elements_located(self.items_inventario)) 
        productos = self.driver.find_elements(*self.items_inventario)
        return productos
    
    def obtener_nombres_productos(self):
        productos = self.driver.find_elements(*self.items_inventario_nombre)
        return [producto_nombre.text for producto_nombre in productos]
    
    def agregar_primer_producto(self):
        productos = self.wait.until(EC.visibility_of_all_elements_located(self.items_inventario)) 

        primer_boton_producto = productos[0].find_element(*self.boton_agregar_carrito)
        primer_boton_producto.click()

    def agregar_producto_por_nombre(self,nombre_producto):

        productos = self.driver.find_elements(*self.items_inventario)   

        for producto in productos:
            nombre = producto.find_element(*self.items_inventario_nombre).text

            if nombre.strip() == nombre_producto.strip():
                boton = producto.find_element(*self.boton_agregar_carrito)
                boton.click()
                return self
        
        raise Exception(f"No se encontro el producto {nombre_producto}")
            
    def abrir_carrito(self):
        self.wait.until(EC.element_to_be_clickable(self.enlace_carrito)).click()
        return self
    
    def obtener_conteo_carrito(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.contador_carrito)) 
            contador_carrito = self.driver.find_element(*self.contador_carrito)
            return int(contador_carrito.text)
        except:
            return 0