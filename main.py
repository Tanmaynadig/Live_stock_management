from flask import Flask, request, jsonify, session
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)

USER_CREDENTIALS = {
    'username': 'admin',
    'password': 'admin123'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Jalagara@6106',
            database='livestock_management'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if USER_CREDENTIALS.get('username') == username and USER_CREDENTIALS.get('password') == password:
        session['user'] = username
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/add_animal', methods=['POST'])
def add_animal():
    data = request.json
    try:
        connection = get_db_connection()
        if connection is None:
            raise Error("Failed to connect to the database.")
        
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO Animal (AnimalID, Species, Breed, Sex, Status, BreederID)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (data['AnimalID'], data['Species'], data['Breed'], data['Sex'], data['Status'], data['BreederID'] ))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Animal added successfully'})
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/list_animals', methods=['GET'])
def list_animals():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Animal")
        animals = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(animals)
    except Error as e:
        return jsonify({'error': str(e)}), 500
@app.route('/search_animals', methods=['GET'])    
def search_animal(species):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Animal where species = %s",(species,))
        animal = cursor.fetchone()
        cursor.close()
        connection.close()
        return jsonify(animal)
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_animal/<int:id>', methods=['DELETE'])
def delete_animal(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        delete_query = "DELETE FROM Animal WHERE AnimalID = %s"
        cursor.execute(delete_query, (id,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Animal deleted successfully'})
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/total_animals', methods=['GET'])
def total_animals():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as total FROM Animal")
        total = cursor.fetchone()
        cursor.close()
        connection.close()
        return jsonify(total)
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/total_animals_by_species/<species>', methods=['GET'])
def total_animals_by_species(species):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as total FROM Animal WHERE Species = %s", (species,))
        total = cursor.fetchone()
        cursor.close()
        connection.close()
        return jsonify(total)
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list_medication', methods=['GET'])
def list_medication():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Medication")
        medication = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(medication)
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list_feed', methods=['GET'])
def list_feed():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Feed")
        feed = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(feed)
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/breeds/<species>', methods=['GET'])
def get_breeds(species):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT DISTINCT Breed FROM Animal WHERE Species = %s", (species,))
        breeds = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify([breed['Breed'] for breed in breeds])
    except Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
