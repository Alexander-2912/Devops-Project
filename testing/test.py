import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from pyvirtualdisplay import Display

display = Display(visible=0, size=(300,300))
display.start()

chromedriver_autoinstaller.install()

chrome_options = webdriver.ChromeOptions()

options = [
    "--window-size=1200, 1200",
    "--ignore-certificate-errors"
]

for option in options:
    chrome_options.add_argument(options)

class TestFormElements:
    def setup_class(cls):
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.get("http://localhost:5173/login")

    def teardown_class(cls):
        cls.driver.quit()

    def test_nama_label(self):
        nama_label = self.driver.find_element(By.XPATH, "//label[@for='username']")
        assert nama_label.text == "Username", "pengecekan nama gagal"

    def test_password_label(self):
        password_label = self.driver.find_element(By.XPATH, "//label[@for='password']")
        assert password_label.text == "Password", "pengecekan password gagal"
