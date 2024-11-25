from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Carregar o modelo treinado e as colunas usadas durante o treinamento
with open('modelo_treinado.pkl', 'rb') as file:
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
        # Coletar dados enviados pelo frontend
        data = {
            'num_envolvidos': int(request.form['num_envolvidos']),
            'idade': int(request.form['idade']),
            'categoria_habilitacao': request.form['categoria_habilitacao'],
            'dia_semana': request.form['dia_semana'],
            'hora': int(request.form['hora']),
            'faixa_etaria': request.form['faixa_etaria'],
            'mes': int(request.form['mes']),
            'dia': int(request.form['dia']),
        }
        
        # Preprocessar os dados
        processed_data = preprocess_input(data)
        
        # Realizar a previsão
        prediction = model.predict(processed_data)
        probabilidade = model.predict_proba(processed_data)[0][1]  # Probabilidade de fatalidade
        
        # Retornar o resultado
        resultado = {
            "fatalidade": bool(prediction[0]),
            "probabilidade": round(probabilidade * 100, 2)  # Converter para percentual
        }
        return jsonify(resultado)
    
    except Exception as e:
        # Retornar o erro em formato JSON
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
