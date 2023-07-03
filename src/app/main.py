from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
import pickle
from sklearn import linear_model
import os

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get("BASIC_AUTH_USERNAME")
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get("BASIC_AUTH_PASSWORD")

basic_auth = BasicAuth(app)

colunas = ["tamanho", "ano", "garagem"]
modelo = pickle.load(open('modelo.sav','rb'))


@app.route('/')
def home():
    return "Minha primeira API."

#o código contido no endpoint será executado toda vez que alguém fizer uma requisição
@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    return frase    

#@app.route("/cotacao/<int:tamanho>")
@app.route("/cotacao/", methods=['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    #list comprehension
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])



app.run(debug=True)