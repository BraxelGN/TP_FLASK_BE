from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123w@localhost/pizzeria'
db = SQLAlchemy(app)


class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    tamaño = db.Column(db.String(50), nullable=False)
    toppings = db.Column(db.JSON)

class Empanada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coccion = db.Column(db.String(50), nullable=False)
    ingredientes = db.Column(db.JSON)
    __tablename__ = 'empanadas'  # Agrega esta línea para especificar el nombre de la tabla

# Rutas para pizzas
@app.route('/pizzas', methods=['GET', 'POST', 'PUT', 'DELETE'])
def pizzas():
    if request.method == 'GET':
        # Obtener todas las pizzas o una pizza específica
        pizza_id = request.args.get('id')
        if pizza_id:
            pizza = Pizza.query.get(pizza_id)
            if pizza:
                pizza_json = {"id": pizza.id, "nombre": pizza.nombre, "tamaño": pizza.tamaño, "toppings": pizza.toppings}
                return jsonify(pizza_json)
            else:
                return jsonify({"error": "Pizza no encontrada"}), 404
        else:
            pizzas = Pizza.query.all()
            pizzas_json = [{"id": pizza.id, "nombre": pizza.nombre, "tamaño": pizza.tamaño, "toppings": pizza.toppings} for pizza in pizzas]
            return jsonify(pizzas_json)

    elif request.method == 'POST':
    # Crear una nueva pizza
        data = request.get_json()
        nueva_pizza = Pizza(nombre=data['nombre'], tamaño=data['tamaño'], toppings=data['toppings'])

        try:
            db.session.add(nueva_pizza)
            db.session.commit()
            return jsonify({"message": "Pizza creada exitosamente"}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error durante la creación de la pizza: {e}")
            return jsonify({"error": "Error durante la creación de la pizza"}), 500


    elif request.method == 'PUT':
    # Actualizar una pizza existente
        data = request.get_json()
        pizza_id = data.get('id')
        pizza = Pizza.query.get(pizza_id)

        try:
            if pizza:
                pizza.nombre = data['nombre']
                pizza.tamaño = data['tamaño']
                pizza.toppings = data['toppings']
                db.session.commit()
                return jsonify({"message": "Pizza actualizada exitosamente"}), 200
            else:
                return jsonify({"error": "Pizza no encontrada"}), 404
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error durante la actualización de la pizza: {e}")
            return jsonify({"error": "Error durante la actualización de la pizza"}), 500


    elif request.method == 'DELETE':
    # Eliminar una pizza existente
        pizza_id = request.args.get('id')
        pizza = Pizza.query.get(pizza_id)

    try:
        if pizza:
            db.session.delete(pizza)
            db.session.commit()
            return jsonify({"message": "Pizza eliminada exitosamente"}), 200
        else:
            return jsonify({"error": "Pizza no encontrada"}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error durante la eliminación de la pizza: {e}")
        return jsonify({"error": "Error durante la eliminación de la pizza"}), 500



# Rutas para empanadas
@app.route('/empanadas', methods=['GET', 'POST', 'PUT', 'DELETE'])
def empanadas():
    if request.method == 'GET':
        # Obtener todas las empanadas o una empanada específica
        empanada_id = request.args.get('id')
        if empanada_id:
            empanada = Empanada.query.get(empanada_id)
            if empanada:
                empanada_json = {"id": empanada.id, "coccion": empanada.coccion, "ingredientes": empanada.ingredientes}
                return jsonify(empanada_json)
            else:
                return jsonify({"error": "Empanada no encontrada"}), 404
        else:
            empanadas = Empanada.query.all()
            empanadas_json = [{"id": empanada.id, "coccion": empanada.coccion, "ingredientes": empanada.ingredientes} for empanada in empanadas]
            return jsonify(empanadas_json)

    elif request.method == 'POST':
    # Crear una nueva empanada
        data = request.get_json()
        nueva_empanada = Empanada(coccion=data['coccion'], ingredientes=data['ingredientes'])

        try:
            db.session.add(nueva_empanada)
            db.session.commit()
            return jsonify({"message": "Empanada creada exitosamente"}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error durante la creación de la empanada: {e}")
            return jsonify({"error": "Error durante la creación de la empanada"}), 500


    elif request.method == 'PUT':
        # Actualizar una empanada existente
        data = request.get_json()
        empanada_id = data.get('id')
        empanada = Empanada.query.get(empanada_id)

        if empanada:
            empanada.coccion = data['coccion']
            empanada.ingredientes = data['ingredientes']
            db.session.commit()
            return jsonify({"message": "Empanada actualizada exitosamente"}), 200
        else:
            return jsonify({"error": "Empanada no encontrada"}), 404

    elif request.method == 'DELETE':
    # Eliminar una empanada existente
        empanada_id = request.args.get('id')
        empanada = Empanada.query.get(empanada_id)

        try:
            if empanada:
                db.session.delete(empanada)
                db.session.commit()
                return jsonify({"message": "Empanada eliminada exitosamente"}), 200
            else:
                return jsonify({"error": "Empanada no encontrada"}), 404
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error durante la eliminación: {e}")
            return jsonify({"error": "Error durante la eliminación"}), 500

if __name__ == '__main__':
    app.run(debug=True)
