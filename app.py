from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

# Configuração para iniciar FLask
app = Flask(__name__)
# Configuração de senha para Flask -> Banco de dados
app.config['SECRET_KEY'] = "your_secret_key"
# Endereço do Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql:///root:admin123@127.0.0.1:3306/daily-diet'
# Configuração para Banco de Dados
login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

#view login
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Rota de Login
@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Validação se foi recebido usuário e senha
    if username and password:
        # Login OK
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return jsonify({"message": "Autenticação realizada com sucesso"})
        
    return jsonify({"message": "Credenciais Inválidas"}), 400

# Rota de Logout
@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"})

# Criação de Rota Flask Exemplo
@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello world"


# Start Flask Server
if __name__ == '__main__':
    app.run(debug=True)
