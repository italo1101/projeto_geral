import unittest
import pandas as pd

# Supondo que você tenha suas funções ou mapeamentos em um módulo específico
from app import sexo_map, cinto_map, embreg_map, categoria_map, veiculo_map, dia_semana_map

class TestUnitarios(unittest.TestCase):
    
    def test_sexo_map(self):
        self.assertEqual(sexo_map.get('Feminino', 0), 1)
        self.assertEqual(sexo_map.get('Masculino', 0), 2)
        self.assertEqual(sexo_map.get('Outro', 0), 0)  # Valor padrão para mapeamento inválido

    def test_cinto_map(self):
        self.assertEqual(cinto_map.get('SIM', 0), 1)
        self.assertEqual(cinto_map.get('NÃO', 0), 0)
        self.assertEqual(cinto_map.get('Talvez', 0), 0)  # Valor padrão para mapeamento inválido

    def test_categoria_habilitacao_map(self):
        self.assertEqual(categoria_map.get('B', 13), 6)
        self.assertEqual(categoria_map.get('AE', 13), 4)
        self.assertEqual(categoria_map.get('Desconhecido', 13), 10)
        self.assertEqual(categoria_map.get('INEXISTENTE', 13), 13)  # Valor padrão

    def test_dataframe_creation(self):
        # Testa se o DataFrame é criado corretamente com os valores de entrada
        input_data = pd.DataFrame([[1, 1, 2, 1, 2, 6, 0, 30, 12, 3]],
                                  columns=['num_envolvidos', 'condutor', 'sexo', 'cinto_seguranca', 
                                           'Embreagues', 'categoria_habilitacao', 'especie_veiculo', 
                                           'Idade', 'hora', 'dia_semana'])
        self.assertEqual(input_data.shape, (1, 10))  # Apenas 1 linha com 10 colunas
        self.assertEqual(input_data['sexo'][0], 2)

if __name__ == '_main_':
    unittest.main()