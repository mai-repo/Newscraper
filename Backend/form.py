from flask import Blueprint, request, jsonify
import sqlite3

form_bp = Blueprint('form', __name__)


def create_add_fav():
    with sqlite3.connect('news.db') as connection:
        cursor = connection.cursor()
        cursor.execute
        # Create the favorites table referencing news.id
        cursor.execute('''CREATE TABLE IF NOT EXISTS favArt (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            news_id INTEGER NOT NULL,
                            FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE)''')
        connection.commit()

# Call the function to initialize the database
create_add_fav()

# Handle GET request to retrieve favorite articles
@form_bp.route('/favorites', methods=['GET'])
def get_favorites():
    with sqlite3.connect('news.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM favArt')
        favorites = cursor.fetchall()

    return jsonify(favorites), 200

# Handle POST request to add favorite articles
@form_bp.route('/favorites', methods=['POST'])
def add_favorite():
    data = request.get_json()
    username = data.get('username')
    news_id = data.get('news_id')

    if not username or not news_id:
        return {'error': 'Username and news_id are required'}, 400

    with sqlite3.connect('news.db') as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO favArt (username, news_id) VALUES (?, ?)', (username, news_id))
        connection.commit()

    return {'message': 'Favorite added successfully'}, 201

@form_bp.route('/editFavorites/<int:id>', methods=['PUT'])
def edit_favorites(id):
    """Update a favorite entry in favArt."""
    data = request.get_json()
    username = data.get('username')

    if not username:
        return {'error': 'Username is required'}, 400

    with sqlite3.connect('news.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''UPDATE favArt
                            SET username = ?
                            WHERE id = ?''', (username, id))
        if cursor.rowcount == 0:
            return {'error': 'Favorite not found'}, 404

        connection.commit()

    return {'message': 'Favorite updated successfully'}, 200

@form_bp.route('/deleteFavorite/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    with sqlite3.connect('news.db') as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM favArt WHERE id = ?', (id,))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Favorite not found'}), 404

        connection.commit()
    return jsonify({'message': 'Favorite deleted successfully'}), 200