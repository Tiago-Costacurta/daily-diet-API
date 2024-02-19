from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt

# Configuração para iniciar FLask
app = Flask(__name__)
# Configuração de senha para Flask -> Banco de dados
app.config['SECRET_KEY'] = "your_secret_key"
# Endereço do Banco de Dados
# SQLITE
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# MYSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet'
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

        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
            return jsonify({"message": "Autenticação realizada com sucesso"})
        
    return jsonify({"message": "Credenciais Inválidas"}), 400

# Rota de Logout
@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"})

@app.route('/user', methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso"})

    return jsonify({"message": "Dados inválidos"}), 400

# Criação de Rota Flask Exemplo
#@app.route("/hello-world", methods=["GET"])
#def hello_world():
    return "Hello world"

# Read de usuários
@app.route('/user/<int:id_user>', methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return  jsonify({"username": user.username})
    
    return jsonify({"message": "Usuário não encontrado"}), 404

# Atualização de Usuários
@app.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == "user":
        return jsonify({"message": "Operação não permitida"}), 403
    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} atualizado com sucesso"})

    return jsonify({"message": "Usuário não encontrado"}), 404

# Deleção de Usuários
@app.route('/user/<int:id_user>', methods=["GET"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if current_user.role != 'admin':
        return jsonify({"message": "Operação não permitida"}), 403
    if id_user == current_user.id:
        return jsonify({"message": "Deleção não permitida"}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} deletado com sucesso"})

    return jsonify({"message": "Usuário não encontrado"}), 404


# Start Flask Server
if __name__ == '__main__':
    app.run(debug=True)
