from flask import Flask, render_template, request
import pickle
import pandas as pd

# Inicializa o Flask
app = Flask(__name__)

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
faixa_etaria_map = {'0-17': 0, '18-24': 1, '25-34': 2, '35-44': 3, '45-54': 4, '55-64': 5, '65+': 6}
dia_semana_map = {'domingo': 0, 'segunda': 4, 'terca': 6, 'quarta': 1, 'quinta': 2, 'sexta': 5, 'sabado': 3}
pedestre_map = {'N': 0, 'S': 1, 'sem informação': 2}
passageiro_map = {'N': 0, 'S': 1, 'sem informação': 2}

# Página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Página para fazer a previsão
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Capturar os dados enviados pelo usuário e mapear para valores numéricos
        num_envolvidos = float(request.form['num_envolvidos']) if request.form['num_envolvidos'] else 0
        condutor = float(request.form['condutor']) if request.form['condutor'] else 0
        sexo = sexo_map.get(request.form['sexo'], 0)  # Mapear para numérico
        cinto_seguranca = cinto_map.get(request.form['cinto_seguranca'], 0)  # Mapear para numérico
        embreagues = embreg_map.get(request.form['Embreagues'], 0)  # Mapear para numérico
        categoria_habilitacao = categoria_map.get(request.form['categoria_habilitacao'], 13)  # Mapear para numérico
        especie_veiculo = veiculo_map.get(request.form['especie_veiculo'], 0)  # Mapear para numérico
        idade = float(request.form['Idade']) if request.form['Idade'] else 0
        hora = float(request.form['hora']) if request.form['hora'] else 0
        dia_semana = dia_semana_map.get(request.form['dia_semana'], 0)  # Mapear para numérico

        # Criar um DataFrame com os dados recebidos
        input_data = pd.DataFrame([[num_envolvidos, condutor, sexo, cinto_seguranca, embreagues, 
                                    categoria_habilitacao, especie_veiculo, idade, hora, dia_semana]],
                                  columns=['num_envolvidos', 'condutor', 'sexo', 'cinto_seguranca', 
                                           'Embreagues', 'categoria_habilitacao', 'especie_veiculo', 
                                           'Idade', 'hora', 'dia_semana'])

        # Fazer a previsão com o modelo, se o modelo foi carregado corretamente
        if model:
            prediction = model.predict(input_data)
            # Mapear a previsão para o nome da classe
            if prediction == 0:
                result = 'Não Fatal'
            elif prediction == 1:
                result = 'Fatal'
            else:
                result = 'Sem Ferimentos'
        else:
            result = 'Erro ao carregar o modelo.'

    except Exception as e:
        result = f'Ocorreu um erro ao processar a previsão: {e}'

    # Retornar o resultado para o usuário
    return render_template('index.html', prediction_text=f'A severidade do acidente é: {result}')

# Rodar a aplicação Flask
if __name__ == "__main__":
    app.run(debug=True)