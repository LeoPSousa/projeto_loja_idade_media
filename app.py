import json
import os
from flask import Flask, jsonify, request
from config import DevelopmentConfig, ProductionConfig


produtos = []

def create_app():

    app = Flask(__name__)

    # pega o ambiente da variável de ambiente, default = dev
    env = os.environ.get("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object(ProductionConfig)
        # Agora sim pode validar a SECRET_KEY
        if not app.config["SECRET_KEY"]:
            raise ValueError("SECRET_KEY não definida! Configure no .env ou nas variáveis do servidor.")
    else:
        app.config.from_object(DevelopmentConfig)

    carregar_produtos()

    #registrar rotas
    registrar_rotas(app)

    return app

def carregar_produtos():
    global produtos
    try:
        with open("flask8_products.json", "r", encoding="utf-8") as file:
            produtos = json.load(file)
    except FileNotFoundError:
        print("Produtos não encontrados, iniciando lista vazia.")

def save_all():
    with open("flask8_products.json", "w", encoding="utf-8") as file:
        json.dump(produtos, file, indent=4, ensure_ascii=False)

def registrar_rotas(app):
    #Listar todos os produtos
    @app.route("/products", methods=["GET"])
    def listar_todos():
        return jsonify(produtos)
    
    #Adicionar um novo produto
    @app.route("/products", methods=["POST"])
    def adicionar_produto():
        novo_produto = request.json
        produtos.append(novo_produto)
        save_all()
        return jsonify({"Mensagem": "Produto adicionado com sucesso!"}), 201

    #Atualizar produto
    @app.route("/products", methods=["PUT"])
    def atualizar_produto(id):
        dados_atualizados = request.get_json()
        for produto in produtos:
            if produto.get("id") == id:
                produto.update(dados_atualizados)
                save_all()
                return jsonify({"Mensagem": "Produto atualizado com sucesso!"}), 200
        return jsonify({"Erro": "Produto não encontrado"}), 404
    
    #Deletar um produto
    @app.route("/products", methods=["DELETE"])
    def deletar_produto(id):
        for produto in produtos:
            if produto.get("id") == id:
                produtos.remove(produto)
                save_all()
                return jsonify({"Mensagem": "Produto removido com sucesso!"}), 200
        return jsonify({"Erro": "Produto não encontrado"}), 404
    
    

if __name__ == "__main__":
    app = create_app()
    app.run()