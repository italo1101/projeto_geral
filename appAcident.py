from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Carregar o modelo treinado e as colunas usadas durante o treinamento
with open('rls_accident_model.pkl', 'rb') as file:
    model, model_columns = pickle.load(file)

# Função para converter a entrada do formulário em formato adequado para o modelo
def preprocess_input(data):
    # Criar um DataFrame com as colunas esperadas
    df = pd.DataFrame(data, index=[0])
    
    # Converte as colunas categóricas em variáveis dummy
    df = pd.get_dummies(df, drop_first=True)
    
    # Adiciona colunas ausentes com valor 0
    for col in model_columns:
        if col not in df.columns:
            df[col] = 0
    
    # Garantir que todas as colunas esperadas estejam presentes
    df = df[model_columns]
    
    return df

@app.route('/')
def home():
    return render_template('index.html')  # Alterado para o formulário de acidentes

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Coletar dados do formulário
        data = {
            'Year': int(request.form['Year']),
            'Location': request.form['Location'],  # Exemplo de nova variável
            'Severity': int(request.form['Severity']),  # Exemplo de nova variável
            # Adicione outras variáveis conforme necessário
        }
        
        # Convertendo para o formato adequado
        processed_data = preprocess_input(data)
        
        # Realizar a previsão
        prediction = model.predict(processed_data)
        
        # Retornar o resultado
        return f'A previsão da severidade do acidente é: {prediction[0]}'
    except Exception as e:
        # Log de erro
        return f'Ocorreu um erro: {e}'

if __name__ == '__main__':
    app.run(debug=True)