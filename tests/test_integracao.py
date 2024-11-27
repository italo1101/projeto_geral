import unittest
from app import app

class TestIntegracao(unittest.TestCase):
    
    def setUp(self):
        # Inicializa o cliente de teste Flask
        self.client = app.test_client()
        self.client.testing = True

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)  
        self.assertIn(b'<title>Data Crash</title>', response.data)

    def test_predict_valid_input(self):
        # Teste para entrada válida
        response = self.client.post(
            '/predict',
            data={
                'num_envolvidos': 2,
                'condutor': 1,
                'sexo': 'Masculino',
                'cinto_seguranca': 'SIM',
                'Embreagues': 'SIM',
                'categoria_habilitacao': 'AB',
                'especie_veiculo': 'Automóvel',
                'Idade': 25,
                'hora': 15,
                'dia_semana': 'segunda'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'severidade do acidente', response.data.lower())

    def test_predict_invalid_input(self):
        # Teste para entrada inválida
        response = self.client.post(
            '/predict',
            data={
                'num_envolvidos': 'invalido',
                'condutor': 1,
                'sexo': 'Masculino',
                'cinto_seguranca': 'SIM',
                'Embreagues': 'SIM',
                'categoria_habilitacao': 'AB',
                'especie_veiculo': 'Automóvel',
                'Idade': 25,
                'hora': 15,
                'dia_semana': 'segunda'
            }
        )
        self.assertNotEqual(response.status_code, 400)
        self.assertIn(
            b'erro',
            response.data.lower(),
            msg=f"Resposta inesperada: {response.data}"
        )


if __name__ == '_main_':
    unittest.main()