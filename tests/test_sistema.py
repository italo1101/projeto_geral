import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class TestSistema(unittest.TestCase):
    def setUp(self):
        # Usando o ChromeDriverManager para gerenciar o ChromeDriver automaticamente
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("http://127.0.0.1:5000")  # URL do aplicativo Flask rodando localmente

    def test_status_sistema(self):
        """Teste básico para verificar se o sistema está acessível"""
        driver = self.driver
        # Verificar se a página foi carregada corretamente (status da página)
        self.assertEqual(driver.title, "Data Crash")  # Substitua com o título correto da sua página
        # Verificar se a página contém um elemento básico para garantir que carregou
        body = driver.find_element(By.TAG_NAME, "body")
        self.assertIsNotNone(body)

    def tearDown(self):
        """Fecha o navegador após o teste"""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
