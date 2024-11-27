import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

class TestSistema(unittest.TestCase):
    def setUp(self):
        # Usando o ChromeDriverManager para gerenciar o ChromeDriver automaticamente
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("http://127.0.0.1:5000")  # URL do aplicativo Flask rodando localmente

    def test_titulo_pagina(self):
        """Teste se o título da página está correto"""
        self.assertEqual(self.driver.title, "Data Crash")

    def test_navegacao_menu(self):
        """Teste da navegação pelos links do menu"""
        driver = self.driver
        sobre_link = driver.find_element(By.LINK_TEXT, "Sobre")
        sobre_link.click()
        sleep(1)
        self.assertIn("#sobre", driver.current_url)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
