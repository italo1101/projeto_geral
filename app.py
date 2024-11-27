from flask import Flask, render_template, request, jsonify
from flasgger import Swagger
import pickle
import pandas as pd

# Inicializa o Flask
app = Flask(__name__)
swagger = Swagger(app)  # Inicializa o Flasgger com o app Flask

# Carregar o modelo treinado
try:
    with open('xgboost_model.pkl', 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    model = None

# Mapear as opções para números
sexo_map = {'Feminino': 1, 'Masculino': 2, 'Desconhecido': 0}
cinto_map = {'SIM': 1, 'NÃO': 0}
embreg_map = {'SIM': 2, 'NÃO': 0, 'NÃO INFORMADO': 1}
categoria_map = {
    'A': 0, 'AB': 1, 'AC': 2, 'AD': 3, 'AE': 4, 'AP': 5,
    'B': 6, 'C': 7, 'D': 8, 'E': 9, 'Desconhecido': 10, 'IN': 11, 'N': 12, 'nan': 13
}
veiculo_map = {'Automóvel': 0, 'Bicicleta': 1, 'Motocicleta': 2, 'Ônibus': 4, 'Outro': 3}
dia_semana_map = {'domingo': 0, 'segunda': 4, 'terca': 6, 'quarta': 1, 'quinta': 2, 'sexta': 5, 'sabado': 3}
condutor_map = {'SIM': 1, 'NÃO': 0}

# Página inicial (para exibir o formulário HTML)
@app.route('/')
def home():
    """
    Exibe o formulário para o usuário preencher.
    ---
    responses:
      200:
        description: Página inicial com o formulário
    """
    return render_template('index.html')

# Página para fazer a previsão
@app.route('/predict', methods=['POST'])
def predict():
    """
    Faz uma previsão sobre a severidade do acidente com base nos dados fornecidos pelo usuário.
    ---
    parameters:
      - name: num_envolvidos
        in: formData
        type: number
        required: true
        description: Número de envolvidos no acidente
      - name: condutor
        in: formData
        type: string
        required: true
        description: Indica se o condutor estava envolvido
        enum:
          - SIM
          - NÃO
      - name: sexo
        in: formData
        type: string
        required: true
        description: Sexo do condutor
        enum:
          - Feminino
          - Masculino
          - Desconhecido
      - name: cinto_seguranca
        in: formData
        type: string
        required: true
        description: O condutor estava usando cinto de segurança
        enum:
          - SIM
          - NÃO
      - name: Embreagues
        in: formData
        type: string
        required: true
        description: Se o veículo tinha embreagem
        enum:
          - SIM
          - NÃO
          - NÃO INFORMADO
      - name: categoria_habilitacao
        in: formData
        type: string
        required: true
        description: Categoria da habilitação do condutor
        enum:
          - A
          - AB
          - AC
          - AD
          - AE
          - AP
          - B
          - C
          - D
          - E
          - Desconhecido
          - IN
          - N
          - nan
      - name: especie_veiculo
        in: formData
        type: string
        required: true
        description: Tipo do veículo envolvido
        enum:
          - Automóvel
          - Bicicleta
          - Motocicleta
          - Ônibus
          - Outro
      - name: Idade
        in: formData
        type: number
        required: true
        description: Idade do condutor
      - name: hora
        in: formData
        type: number
        required: true
        description: Hora do acidente
      - name: dia_semana
        in: formData
        type: string
        required: true
        description: Dia da semana
        enum:
          - domingo
          - segunda
          - terca
          - quarta
          - quinta
          - sexta
          - sabado
    responses:
      200:
        description: Resultado da previsão da severidade do acidente
    """
    try:
        # Capturar os dados enviados pelo usuário e mapear para valores numéricos
        num_envolvidos = float(request.form['num_envolvidos'])
        condutor = condutor_map.get(request.form['condutor'], 0)
        sexo = sexo_map.get(request.form['sexo'], 0)
        cinto_seguranca = cinto_map.get(request.form['cinto_seguranca'], 0)
        embreagues = embreg_map.get(request.form['Embreagues'], 0)
        categoria_habilitacao = categoria_map.get(request.form['categoria_habilitacao'], 13)
        especie_veiculo = veiculo_map.get(request.form['especie_veiculo'], 0)
        idade = float(request.form['Idade'])
        hora = float(request.form['hora'])
        dia_semana = dia_semana_map.get(request.form['dia_semana'], 0)

        # Criar um DataFrame com os dados recebidos
        input_data = pd.DataFrame([[num_envolvidos, condutor, sexo, cinto_seguranca, embreagues,
                                    categoria_habilitacao, especie_veiculo, idade, hora, dia_semana]],
                                  columns=['num_envolvidos', 'condutor', 'sexo', 'cinto_seguranca',
                                           'Embreagues', 'categoria_habilitacao', 'especie_veiculo',
                                           'Idade', 'hora', 'dia_semana'])

        if model:
            prediction = model.predict(input_data)[0]
            result = 'Fatal' if prediction == 1 else 'Não Fatal'
        else:
            result = 'Erro ao carregar o modelo.'

    except Exception as e:
        result = f'Ocorreu um erro: {e}'

    return jsonify({'prediction_text': f'A severidade do acidente é: {result}'})

if __name__ == "__main__":
    app.run(debug=True)
