# daily-diet-API

API desenvolvida para registros diarios de dieta com integração a banco de dados utilizando python e flask.
Desafio Rocketseat.


# Linguagem:
<ul>
    <li>Python</li>
</ul>

# Framework
<ul>
    <li>Flask</li>
    <ul>
        <li>Flask</li>
        <li>request</li>
        <li>jsonify</li>
    </ul>
    <li>Flask-SQLAlchemy</li>
    <li>Flask-Login</li>
    <ul>
        <li>LoginManager</li>
        <li>login_user</li>
        <li>current_user</li>
        <li>UserMixin</li>
        <li>logout_user</li>
        <li>login_required</li>
    </ul>
    <li>Werkzeug</li>
    <li>pymysql</li>
    <li>cryptography</li>
    <li>bcrypt</li>
</ul>

Banco de dados
<ul>
    <li>Mysql</li>
</ul>

Container
<ul>
    <li>Docker</li>
</ul>

# Rotas
<ul>
<li>Login</li>
    
    Route: /login
    { "username": "username", "password": "password"}
    method: POST 

<li>Logout</li>
    
    Route: /logout
    method: GET

<li>Create User</li>
    
    Route /user
    {"username": "username", "password": "password"}
    method: POST
    
<li>Read user</li>

    route /user/<id:user_id>
    method: GET
    
<li>Update User</li>

    route /user/<int:id_user>
    {"password": "password"}
    method: PUT

<li>Delete User</li>
    
    route /user/<int:id_user>
    method: DELETE

<li>Create Diet</li>
    
    route /user/<int:id_user>/diet/create
    {"name": "Nome Refeição", "description": "descrição da refeição", "diet": "está na dieta true ou false"}
    method: POST

<li>Listar todas dietas do usuário</li>
        
    route /user/<int:id_user>/diet/list
    method: GET

<li>Alterar Dieta</li>
    
    route /user/<int:id_user>/diet/change/<int:id_diet>
    method: PUT

<li>Listar uma única dieta</li>
    
    route /user/<int:id_user>/diet/<int:id_diet>
    method: GET

<li>Deletar dieta</li>
    
    route /user/diet/delete
    method: DELETE

</ul>