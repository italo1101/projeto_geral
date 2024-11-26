import unittest
from app import calcular_fatalidade

class TestUnitarios(unittest.TestCase):
    def test_calcular_fatalidade_valores_validos(self):
        """Teste com valores válidos"""
        resultado = calcular_fatalidade(idade=30, num_envolvidos=2, hora=12)
        self.assertEqual(resultado, "Baixa Fatalidade")

    def test_calcular_fatalidade_faixa_horario(self):
        """Teste de valores críticos de horário"""
        resultado = calcular_fatalidade(idade=18, num_envolvidos=1, hora=23)
        self.assertEqual(resultado, "Alta Fatalidade")

    def test_calcular_fatalidade_idade_extrema(self):
        """Teste com idade muito baixa"""
        resultado = calcular_fatalidade(idade=2, num_envolvidos=3, hora=10)
        self.assertEqual(resultado, "Média Fatalidade")

    def test_calcular_fatalidade_envolvidos_0(self):
        """Teste com número de envolvidos igual a 0"""
        resultado = calcular_fatalidade(idade=25, num_envolvidos=0, hora=14)
        self.assertEqual(resultado, "Erro: Número de envolvidos deve ser maior que 0")

    def test_calcular_fatalidade_hora_extrema(self):
        """Teste com hora no limite (00:00)"""
        resultado = calcular_fatalidade(idade=40, num_envolvidos=3, hora=0)
        self.assertEqual(resultado, "Baixa Fatalidade")

    def test_calcular_fatalidade_idade_negativa(self):
        """Teste com idade negativa"""
        resultado = calcular_fatalidade(idade=-5, num_envolvidos=2, hora=10)
        self.assertEqual(resultado, "Erro: Idade inválida")

if __name__ == "_main_":
    unittest.main()