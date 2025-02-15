from flask import Blueprint, request, jsonify
import requests
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

pokemon = Blueprint('pokemon', __name__)

# Function to create the favorite article table if it doesn't exist
def create_add_Pokemon():
    with sqlite3.connect('news.db') as connection:
        cursor = connection.cursor()
        # Create the favorite article table referencing news.id
        cursor.execute('''CREATE TABLE IF NOT EXISTS pokemon (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            pokemonName TEXT NOT NULL,
                            image TEXT NOT NULL)''')
        connection.commit()
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

    with sqlite3.connect('news.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO pokemon (username, pokemonName, image)
                            VALUES (?, ?, ?)''', (username, pokemonName, image))
        connection.commit()

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

    with sqlite3.connect('news.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''UPDATE pokemon
                            SET username = ?, pokemonName = ?, image = ?
                            WHERE id = ?''', (username, pokemonName, image, id))
        connection.commit()

    logger.debug(f"Pokemon with ID {id} updated successfully.")
    return jsonify({"message": "Pokemon updated successfully"}), 200

# Route to delete a Pokemon from the database
@pokemon.route('/deletePokemon/<int:id>', methods=["DELETE"])
def delete_Pokemon(id):
    with sqlite3.connect('news.db') as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM pokemon WHERE id = ?', (id,))
        connection.commit()

    logger.debug(f"Pokemon with ID {id} deleted successfully.")
    return jsonify({"message": "Pokemon deleted successfully"}), 200

# Route to get all Pokemon from the database
@pokemon.route('/getPokemon', methods=["GET"])
def get_all_Pokemon():
    with sqlite3.connect('news.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM pokemon')
        rows = cursor.fetchall()

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

    with sqlite3.connect('news.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM pokemon WHERE id = ?', (pokemon_id,))
        pokemon = cursor.fetchone()

        if not pokemon:
            logger.error("Pokemon not found in profile_photo")
            return jsonify({"error": "Pokemon not found"}), 404

        cursor.execute('''
            UPDATE pokemon
            SET image = ?
            WHERE id = ?
        ''', (image, pokemon_id))
        connection.commit()

    if cursor.rowcount == 0:
        logger.error("Pokemon not found in profile_photo update")
        return jsonify({"error": "Pokemon not found"}), 404

    logger.debug(f"Profile photo for Pokemon with ID {pokemon_id} updated successfully.")
    return jsonify({"message": "Profile photo updated successfully"}), 200
