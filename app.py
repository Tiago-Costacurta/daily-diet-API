from flask import Flask, request, jsonify
from models.user import User
from models.diet import Diet
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt
from timezone import AdjustTimezone

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

@app.route('/user/<int:id_user>/diet/create', methods=["POST"])
@login_required
def create_diet(id_user):
    # name, description, date, snack, id_user
    data = request.json
    name = data.get("name")
    description = data.get("description")
    diet = data.get("diet")

    if id_user == current_user.id or current_user.role == 'admin':
        if name and description:
            dietdb = Diet(name=name, description=description, diet=diet, userid=id_user)
            db.session.add(dietdb)
            db.session.commit()
            return jsonify({"message": "Refeição cadastrada com sucesso"})
    
        return jsonify({"message": "Dados Incorretos"}), 400
    return jsonify({"message": "Operação não permitida"})

# Listagem de dietas conforme o ID do usuário
@app.route('/user/<int:id_user>/diet/list', methods=["GET"])
@login_required
def list_all_diet(id_user):
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == "user":
        return jsonify({"message": "Operação não permitida"}), 403
    
    if user:
        list_diet = db.session.query(Diet).filter(Diet.userid == id_user).all()
        diets_data = []

        for diet in list_diet:
            adjust_date = AdjustTimezone(date=diet.date)

            diet_data = {
                "id": diet.id,
                "name": diet.name,
                "description": diet.description,
                "date": adjust_date,
                "diet": diet.diet
            }
            diets_data.append(diet_data)

        return jsonify(diets_data)
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404

# Listar uma única dieta
@app.route('/user/<int:id_user>/diet/<int:id_diet>', methods=["GET"])
@login_required
def list_diet(id_user, id_diet):
    if id_user == current_user.id or current_user.role == 'admin':
        list_diet = db.session.query(Diet).filter(Diet.id == id_diet).first()
        
        diet_data = {
                "id": list_diet.id,
                "name": list_diet.name,
                "description": list_diet.description,
                "date": list_diet.date,
                "diet": list_diet.diet
            }

        return jsonify(diet_data)

    return jsonify({"message": "Operação inválida"}), 404


# Alteração de dados da dieta
@app.route('/user/<int:id_user>/diet/change/<int:id_diet>', methods=["PUT"])
@login_required
def change_diet(id_user, id_diet):
    data = request.json
    name = data.get('name')
    description = data.get('description')
    date = data.get('date')
    diet = data.get('diet')

    if id_user == current_user.id or current_user.role == 'admin':
        edit_diet = db.session.query(Diet).filter(Diet.id == id_diet).first()
        if name:
            edit_diet.name = name
        
        if description:
            edit_diet.description = description
        
        if date:
            edit_diet.date = date
        
        if diet:
            edit_diet.diet = diet
            
        db.session.commit()
        return jsonify({"message": f"Nome da refeição {edit_diet.name} alterada com sucesso"})

    return jsonify({"message": "Operação inválida"}), 404
    
# Deletar refeições
@app.route('/user/<int:id_user>/diet/delete', methods=["DELETE"])
@login_required
def delete_diet(id_user):
    data = request.json
    id_diet = data.get("id_diet")
    diet = Diet.query.get(id_diet)

    if id_user == current_user.id or current_user.role == 'admin':
        db.session.delete(diet)
        db.session.commit()
        return jsonify({"message": "Dieta deletada com sucesso"})

    return jsonify({"message": "Dieta não encontrada"})

# Start Flask Server
if __name__ == '__main__':
    app.run(debug=True)
