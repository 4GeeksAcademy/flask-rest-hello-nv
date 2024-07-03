"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personaje, Planeta, Vehiculo, Favorito_Personaje, Favorito_Vehiculo, Favorito_Planeta

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/personajes', methods=['GET'])
def get_personajes():
    response_body = {
        "msg": "Hello, this is your GET /personajes response "
    }
    return jsonify(response_body), 200

@app.route('/planetas', methods=['GET'])
def get_planetas():
    response_body = {
        "msg": "Hello, this is your GET /planetas response "
    }
    return jsonify(response_body), 200

@app.route('/vehiculos', methods=['GET'])
def get_vehiculos():
    response_body = {
        "msg": "Hello, this is your GET /vehiculos response "
    }
    return jsonify(response_body), 200


@app.route('/favorito/personaje/<int:personaje_id>', methods=['POST'])
def add_favorito_personaje(personaje_id):
    user_id = 1
    user = User.query.get(user_id)
    if not user:
        return jsonify({"Mensaje": "Usuario no encontrado."}), 404
    
    personaje = Personaje.query.get(personaje_id)
    if not personaje:
        return jsonify({"Mensaje": "Personaje no encontrado."}), 404
    if Favorito_Personaje.query.filter_by(user_id=user_id, personaje_id=personaje_id).first():
        return jsonify({"Mensaje": "Personaje ya existe en favoritos."}), 400
    
    personaje_favorito = Favorito_Personaje(user_id=user_id, personaje_id=personaje_id)
    db.session.add(personaje_favorito)
    db.session.commit()

    return jsonify({"mensaje": "Personaje añadido a favoritos."}), 201

@app.route('/favorito/planeta/<int:planeta_id>', methods=['POST'])
def add_favorito_planeta(planeta_id):
    user_id = 1
    user = User.query.get(user_id)
    if not user:
        return jsonify({"Mensaje": "Usuario no encontrado."}), 404
    
    planeta = Planeta.query.get(planeta_id)
    if not planeta:
        return jsonify({"Mensaje": "Planeta no encontrado."}), 404
    if Favorito_Planeta.query.filter_by(user_id=user_id, planeta_id=planeta_id).first():
        return jsonify({"Mensaje": "Planeta ya existe en favoritos."}), 400
    
    planeta_favorito = Favorito_Planeta(user_id=user_id, planeta_id=planeta_id)
    db.session.add(planeta_favorito)
    db.session.commit()

    return jsonify({"mensaje": "Planeta añadido a favoritos."}), 201

@app.route('/favorito/vehiculo/<int:vehiculo_id>', methods=['POST'])
def add_favorito_vehiculo(vehiculo_id):
    user_id = 1
    user = User.query.get(user_id)
    if not user:
        return jsonify({"Mensaje": "Usuario no encontrado."}), 404
    
    vehiculo = Vehiculo.query.get(vehiculo_id)
    if not vehiculo:
        return jsonify({"Mensaje": "Vehiculo no encontrado."}), 404
    if Favorito_Vehiculo.query.filter_by(user_id=user_id, vehiculo_id=vehiculo_id).first():
        return jsonify({"Mensaje": "Vehiculo ya existe en favoritos."}), 400
    
    vehiculo_favorito = Favorito_Vehiculo(user_id=user_id, vehiculo_id=vehiculo_id)
    db.session.add(vehiculo_favorito)
    db.session.commit()

    return jsonify({"mensaje": "Vehiculo añadido a favoritos."}), 201

@app.route('/user/favoritos', methods=['GET'])
def get_usuario_favorito():
    user_id = 2

    personajes_favoritos = db.session.query(Favorito_Personaje, Personaje)\
        .join(Personaje, Favorito_Personaje.personaje_id == Personaje.id)\
        .filter(Favorito_Personaje.user_id == user_id)\
        .all()

    planetas_favoritos = db.session.query(Favorito_Planeta, Planeta)\
        .join(Planeta, Favorito_Planeta.planeta_id == Planeta.id)\
        .filter(Favorito_Planeta.user_id == user_id)\
        .all()

    vehiculos_favoritos = db.session.query(Favorito_Vehiculo, Vehiculo)\
        .join(Vehiculo, Favorito_Vehiculo.vehiculo_id == Vehiculo.id)\
        .filter(Favorito_Vehiculo.user_id == user_id)\
        .all()

    response = {
        "personajes_favoritos": [
            {
                "id": fav_personaje.id,
                "personaje_id": fav_personaje.personaje_id,
                "nombre_personaje": personaje.nombre,
            }
            for fav_personaje, personaje in personajes_favoritos
        ],
        "planetas_favoritos": [
            {
                "id": fav_planeta.id,
                "planeta_id": fav_planeta.planeta_id,
                "nombre_planeta": planeta.nombre,
            }
            for fav_planeta, planeta in planetas_favoritos
        ],
        "vehiculos_favoritos": [
            {
                "id": fav_vehiculo.id,
                "vehiculo_id": fav_vehiculo.vehiculo_id,
                "nombre_vehiculo": vehiculo.nombre,
            }
            for fav_vehiculo, vehiculo in vehiculos_favoritos
        ]
    }

    return jsonify(response), 200

with app.app_context():
    usuario_existente = User.query.filter_by(email='nelsonalejandrovn@gmail.com').first()
    if not usuario_existente: 
        nuevo_usuario = User(
            nombre='User1', 
            email='nelsonalejandrovn@gmail.com',
            password='123456',
            is_active=True
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

with app.app_context():
    yoda = Personaje.query.filter_by(nombre='Yoda').first()
    if not yoda: 
        yoda = Personaje(
            nombre='Yoda', 
            color_de_ojos='verde',
            color_de_cabello='blanco'
        )
        db.session.add(yoda)

    c3po = Personaje.query.filter_by(nombre='C3po').first()
    if not c3po: 
        c3po = Personaje(
            nombre='C3po', 
            color_de_ojos='verde',
            color_de_cabello='blanco'
        )
        db.session.add(c3po)  

    db.session.commit()

with app.app_context():
    alderan = Planeta.query.filter_by(nombre='Alderan').first()
    if not alderan: 
        alderan = Planeta(
            nombre='Alderan',
            diametro='12500',
            poblacion='200000000'
        )
        db.session.add(alderan)

    tatoonie = Planeta.query.filter_by(nombre='Tatoonie').first()
    if not tatoonie: 
        tatoonie = Planeta(
            nombre='Tatoonie',
            diametro='75000',
            poblacion='545003364'
        )
        db.session.add(tatoonie)  
        
    db.session.commit()

with app.app_context():
    sand_crawler = Vehiculo.query.filter_by(nombre='Sand Crawler').first()
    if not sand_crawler: 
        sand_crawler = Vehiculo(
            nombre='Sand Crawler',
            modelo='Digger crawler',
            capacidad_pasajeros='46'
        )
        db.session.add(sand_crawler)

    t_16_skyhopper = Vehiculo.query.filter_by(nombre='T-16 skyhopper').first()
    if not t_16_skyhopper:
        t_16_skyhopper = Vehiculo(
            nombre='T-16 skyhopper',
            modelo='T-16 skyhopper',
            capacidad_pasajeros=1
        )
        db.session.add(t_16_skyhopper) 
        
    db.session.commit()

@app.route('/favorito/planeta/<int:planeta_id>', methods=['DELETE'])
def delete_favorito_planeta(planeta_id):
    usuario_id = 8  # Usuario de prueba con ID 8
    usuario = User.query.get(usuario_id)
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    favorito_planeta = Favorito_Planeta.query.filter_by(user_id=usuario_id, planeta_id=planeta_id).first()
    if not favorito_planeta:
        return jsonify({"message": "El planeta no es favorito del usuario"}), 404
    
    try:
        db.session.delete(favorito_planeta)
        db.session.commit()
        return jsonify({"message": "Planeta eliminado de favoritos"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error eliminando el planeta de favoritos: {str(e)}"}), 500

@app.route('/favorito/personaje/<int:personaje_id>', methods=['DELETE'])
def delete_favorito_personaje(personaje_id):
    usuario_id = 8  # Usuario de prueba con ID 8
    usuario = User.query.get(usuario_id)
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    favorito_personaje = Favorito_Personaje.query.filter_by(user_id=usuario_id, personaje_id=personaje_id).first()
    if not favorito_personaje:
        return jsonify({"message": "El personaje no es favorito del usuario"}), 404
    
    try:
        db.session.delete(favorito_personaje)
        db.session.commit()
        return jsonify({"message": "Personaje eliminado de favoritos"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error eliminando el personaje de favoritos: {str(e)}"}), 500

@app.route('/favorito/vehiculo/<int:vehiculo_id>', methods=['DELETE'])
def delete_favorito_vehiculo(vehiculo_id):
    usuario_id = 8  # Usuario de prueba con ID 8
    usuario = User.query.get(usuario_id)
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    favorito_vehiculo = Favorito_Vehiculo.query.filter_by(user_id=usuario_id, vehiculo_id=vehiculo_id).first()
    if not favorito_vehiculo:
        return jsonify({"message": "El vehiculo no es favorito del usuario"}), 404
    
    try:
        db.session.delete(favorito_vehiculo)
        db.session.commit()
        return jsonify({"message": "Vehiculo eliminado de favoritos"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error eliminando el vehiculo de favoritos: {str(e)}"}), 500

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)