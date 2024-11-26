import unittest
import pickle
from app import app

class TestIntegracao(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_modelo_carregamento(self):
        """Teste se o modelo treinado está carregando corretamente"""
        with open("xgboost_model.pkl", "rb") as f:
            modelo = pickle.load(f)
        self.assertIsNotNone(modelo)

    def test_previsao_modelo(self):
        """Teste de previsão do modelo treinado"""
        dados = [25, 2, 15]  # Exemplo de entrada para o modelo
        with open("xgboost_model.pkl", "rb") as f:
            modelo = pickle.load(f)
        previsao = modelo.predict([dados])
        self.assertIn(previsao[0], ["Baixa", "Média", "Alta"])

    def test_endpoint_previsao(self):
        """Teste do endpoint de previsão"""
        response = self.app.post(
            "/predict", 
            json={"idade": 25, "num_envolvidos": 2, "hora": 15}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.json["fatalidade"], ["Baixa", "Média", "Alta"])

if __name__ == "_main_":
    unittest.main()