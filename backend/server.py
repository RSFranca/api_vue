# server.py
from flask import Flask, request, jsonify
import pandas as pd
from fuzzywuzzy import fuzz

app = Flask(__name__)

# Carrega os dados do CSV
df = pd.read_csv('C:/Users/SAMSUNG/git/IntuitiveCara/Teste4/api_vue/backend/Relatorio_cadop.csv', encoding='utf-8', delimiter=';', on_bad_lines='skip')
@app.route('/api/busca', methods=['GET'])
def buscar_operadoras():
    termo = request.args.get('termo', '')
    limite = int(request.args.get('limite', 70))
    
    if not termo:
        return jsonify({"erro": "Parâmetro 'termo' é obrigatório"}), 400
    
    resultados = []
    for _, linha in df.iterrows():
        # Busca em múltiplos campos
        nome_score = fuzz.partial_ratio(termo.lower(), str(linha['Razao_Social']).lower())
        reg_score = fuzz.partial_ratio(termo.lower(), str(linha['Registro_ANS']).lower())
        score_maximo = max(nome_score, reg_score)
        
        if score_maximo >= limite:
            resultados.append({
                "relevancia": score_maximo,
                "dados": linha.to_dict()
            })
    
    # Ordena por relevância
    resultados.sort(key=lambda x: x['relevancia'], reverse=True)
    
    return jsonify({
        "termo_busca": termo,
        "quantidade": len(resultados),
        "resultados": [r['dados'] for r in resultados]
    })

if __name__ == '__main__':
    app.run(debug=True)