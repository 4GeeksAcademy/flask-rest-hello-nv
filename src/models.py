from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "password": self.password,
            "is_active": self.is_active


        }

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_login = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    def serialize(self):
        return {
            "fecha_login": self.fecha_login,
            "user_id": self.user_id
        }

class Personaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    color_de_ojos = db.Column(db.String(250), nullable=False)
    color_de_cabello = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "color_de_ojos": self.color_de_ojos,
            "color_de_cabello": self.color_de_cabello
        }

class Favorito_Personaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    personaje_id = db.Column(db.Integer, db.ForeignKey('personaje.id'))
    personaje = db.relationship("Personaje")
    user = db.relationship("User")

    def serialize(self):
        return {
            "id": self.id
        }

class Planeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    diametro = db.Column(db.String(250), nullable=False)
    poblacion = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "diametro": self.diametro,
            "poblacion": self.poblacion
        }

class Favorito_Planeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planeta_id = db.Column(db.Integer, db.ForeignKey('planeta.id'))
    planeta = db.relationship("Planeta")
    user = db.relationship("User")

    def serialize(self):
        return {
            "id": self.id
        }

class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    modelo = db.Column(db.String(250), nullable=False)
    capacidad_pasajeros = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "modelo": self.modelo,
            "capacidad_pasajeros": self.capacidad_pasajeros
        }

class Favorito_Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculo.id'))
    vehiculo = db.relationship("Vehiculo")
    user = db.relationship("User")

    def serialize(self):
        return {
            "id": self.id
        }