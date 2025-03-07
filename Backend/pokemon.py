from flask import Blueprint, request, jsonify
import requests
import psycopg2
import logging
from Backend.config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

pokemon = Blueprint('pokemon', __name__)

def get_db_connection():
    connection = psycopg2.connect(Config.DATABASE_URL)
    return connection

# Function to create the Pokemon table if it doesn't exist
def create_add_Pokemon():
    connection = get_db_connection()
    cursor = connection.cursor()
    # Create the Pokemon table
    cursor.execute('''CREATE TABLE IF NOT EXISTS pokemon (
                        id SERIAL PRIMARY KEY,
                        username TEXT NOT NULL,
                        pokemonName TEXT NOT NULL,
                        image TEXT NOT NULL)''')
    connection.commit()
    connection.close()
    logger.debug("Pokemon table created or already exists.")

# Call the function to initialize the database
create_add_Pokemon()

base_url = "https://pokeapi.co/api/v2"

# Route to get Pokemon details from the API
@pokemon.route('/catchEm', methods=["GET"])
def get_Pokemon():
    name = request.args.get('name')
    if not name:
        logger.error("Missing 'name' parameter")
        return jsonify({"error": "Missing 'name' parameter"}), 400

    url = f'{base_url}/pokemon/{name.lower()}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        pokemon_name = data['name']
        image_url = data['sprites']['front_default']

        logger.debug(f"Pokemon {pokemon_name} details fetched successfully.")
        return jsonify({
            "pokemonName": pokemon_name,
            "image": image_url
        })
    else:
        logger.error("Pokemon not found")
        return jsonify({"error": "Pokemon not found"}), 404

# Route to save a Pokemon to the database
@pokemon.route('/savePokemon', methods=["POST"])
def save_Pokemon():
    data = request.get_json()
    username = data.get('username')
    pokemonName = data.get('pokemonName')
    image = data.get('image')

    if not username or not pokemonName or not image:
        logger.error("Missing data in save_Pokemon")
        return jsonify({"error": "Missing data"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO pokemon (username, pokemonName, image)
                      VALUES (%s, %s, %s)''', (username, pokemonName, image))
    connection.commit()
    connection.close()

    logger.debug(f"Pokemon {pokemonName} saved successfully.")
    return jsonify({"message": "Pokemon saved successfully"}), 201

# Route to update a Pokemon in the database
@pokemon.route('/updatePokemon/<int:id>', methods=["PUT"])
def update_Pokemon(id):
    data = request.get_json()
    username = data.get('username')
    pokemonName = data.get('pokemonName')
    image = data.get('image')

    if not username or not pokemonName or not image:
        logger.error("Missing data in update_Pokemon")
        return jsonify({"error": "Missing data"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''UPDATE pokemon
                      SET username = %s, pokemonName = %s, image = %s
                      WHERE id = %s''', (username, pokemonName, image, id))
    connection.commit()
    connection.close()

    logger.debug(f"Pokemon with ID {id} updated successfully.")
    return jsonify({"message": "Pokemon updated successfully"}), 200

# Route to delete a Pokemon from the database
@pokemon.route('/deletePokemon/<int:id>', methods=["DELETE"])
def delete_Pokemon(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM pokemon WHERE id = %s', (id,))
    connection.commit()
    connection.close()

    logger.debug(f"Pokemon with ID {id} deleted successfully.")
    return jsonify({"message": "Pokemon deleted successfully"}), 200

# Route to get all Pokemon from the database
@pokemon.route('/getPokemon', methods=["GET"])
def get_all_Pokemon():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM pokemon')
    rows = cursor.fetchall()
    connection.close()

    pokemons = []
    for row in rows:
        pokemons.append({
            "id": row[0],
            "username": row[1],
            "pokemonName": row[2],
            "image": row[3]
        })

    logger.debug("Fetched all Pokemon from the database.")
    return jsonify(pokemons), 200

# Route to change the profile photo of a Pokemon
@pokemon.route('/changeProfile', methods=["PUT"])
def profile_photo():
    data = request.get_json()
    if not data:
        logger.error("Invalid JSON data in profile_photo")
        return jsonify({"error": "Invalid JSON data"}), 400

    image = data.get('image')
    pokemon_id = data.get('pokemon_id')

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM pokemon WHERE id = %s', (pokemon_id,))
    pokemon = cursor.fetchone()

    if not pokemon:
        logger.error("Pokemon not found in profile_photo")
        connection.close()
        return jsonify({"error": "Pokemon not found"}), 404

    cursor.execute('''
        UPDATE pokemon
        SET image = %s
        WHERE id = %s
    ''', (image, pokemon_id))
    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        logger.error("Pokemon not found in profile_photo update")
        return jsonify({"error": "Pokemon not found"}), 404

    logger.debug(f"Profile photo for Pokemon with ID {pokemon_id} updated successfully.")
    return jsonify({"message": "Profile photo updated successfully"}), 200
