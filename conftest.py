import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from decouple import Csv, config

import pathlib
from datetime import datetime
import time

target = pathlib.Path("reports/screens")
target.mkdir(parents=True, exist_ok=True)

# Toma la Api key desde el archivo .env para reqres.in...
API_KEY = config("API_KEY")

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

@pytest.fixture
def login_in_driver(driver):
    LoginPage(driver).abrir()
    return driver

@pytest.fixture
def url_base():
    return "https://reqres.in/api/users"

@pytest.fixture
def header_request():
    return {"x-api-key": API_KEY}

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item,call):
    outcome = yield

    report = outcome.get_result()

    if report.when in ("setup","call") and report.failed:
        driver = item.funcargs.get("driver",None)
        
        if driver:
            timestamp_comun= datetime.now().strftime("%Y%m%d_%H%M%S")
            timestamp_unix = int(time.time())
            file_name= target / f"{report.when}_{item.name}_{timestamp_unix}.png"
            driver.save_screenshot(str(file_name))