from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuração para iniciar FLask
app = Flask(__name__)
# Configuração de senha para Flask -> Banco de dados
app.config['SECRET_KEY'] = "your_secret_key"
# Endereço do Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql:///root:admin123@127.0.0.1:3306/daily-diet'
# Configuração para Banco de Dados
db = SQLAlchemy(app)





# Criação de Rota Flask Exemplo
@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello world"


# Start Flask Server
if __name__ == '__main__':
    app.run(debug=True)