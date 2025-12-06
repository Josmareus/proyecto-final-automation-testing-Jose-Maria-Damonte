# Entrega Proyecto Final - Automation Testing - José María Damonte

Repositorio para proyecto del curso de Automatización QA de Talento Tech 2025.
Se implementan pruebas automatizadas para el sitio SauceDemo, mediante la utilización de Selenium WebDriver y Python.
También se emplea la automatización de pruebas de API, usando un endpoint en [ReqRes](https://app.reqres.in/ "ReqRes's Homepage")

## Propósito del Proyecto

El objetivo para la entrega final es automatizar los flujos de uso del sitio web, para representar las interacciones de un usuario:

- Login con credenciales válidas e inválidas
- Verificación del catálogo de productos
- Interacción con el carrito de compras (añadir productos y verificar su contenido)

Para las verificaciones de API endpoint, se comprueba:

- Obtener un usuario (GET)
- Crear un nuevo usuario (POST)
- Eliminar usuario (DELETE)

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal.
- **Pytest**: Framework de testing para realizar las pruebas y validaciones.
- **Selenium**: Para la automatización de las interacciones con la interfaz web, empleando Chrome WebDriver.
- **Git/GitHub**: Para control de versiones y compartir el código en un repositorio.
- **Request**: Librería para realizar las peticiones REST al API endpoint de ReqRes

## Instalación de Dependencias

1. Asegurarse de tener Python 3.7 o superior instalado.
2. Crear un entorno virtual (python venv y el nombre del entorno, en este caso "env"): `py -m venv env`
3. Activar el entorno virtual: `.\env\Scripts\activate`
4. Instala las dependencias necesarias desde el archivo "requirements.txt":

Estando en la raiz del proyecto, `py -m pip install -r requirements.txt`

5. Modificar el archivo .env.example, quitándole la extencióin .example para que quede solo .env, y dentro colocar la API Key obtenida en el dashboard de ReqRes (es necesario una cuenta gratis).

## Ejecución de Pruebas

Desde la raiz del proyecto: `py run_tests.py`

## Autor
José María Damonte