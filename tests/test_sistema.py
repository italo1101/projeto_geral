import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

class TestSistema(unittest.TestCase):
    def setUp(self):
        """Configura o ambiente de testes antes de cada teste"""
        # Usando o ChromeDriverManager para gerenciar o ChromeDriver automaticamente
        service = Service(ChromeDriverManager().install())
        
        # Configurações do Chrome para rodar em modo headless no CI
        options = Options()
        options.add_argument('--headless')  # Modo headless
        options.add_argument('--no-sandbox')  # Necessário no ambiente CI
        options.add_argument('--disable-dev-shm-usage')  # Necessário no ambiente CI
        options.add_argument('--remote-debugging-port=9222')  # Necessário para depuração remota (caso precise)

        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("http://127.0.0.1:5000")  # URL do aplicativo Flask rodando localmente

    def test_titulo_pagina(self):
        """Teste básico para verificar o título da página"""
        self.assertEqual(self.driver.title, "Data Crash")

    def test_formulario_fatalidade(self):
        """Teste do formulário de cálculo de fatalidade"""
        driver = self.driver
        driver.find_element(By.ID, "num_envolvidos").send_keys("3")
        driver.find_element(By.ID, "idade").send_keys("25")
        driver.find_element(By.ID, "hora").send_keys("13:00")
        driver.find_element(By.ID, "calcular-fatalidade").click()
        sleep(2)  # Aguarde o cálculo
        resultado = driver.find_element(By.ID, "resultado-fatalidade").text
        self.assertIn("Taxa de Fatalidade", resultado)

    def test_navegacao_menu(self):
        """Teste da navegação pelos links do menu"""
        driver = self.driver
        sobre_link = driver.find_element(By.LINK_TEXT, "Sobre")
        sobre_link.click()
        sleep(1)
        self.assertIn("#sobre", driver.current_url)

    def tearDown(self):
        """Fecha o navegador após os testes"""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
