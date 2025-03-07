from flask import Blueprint, request, jsonify
import psycopg2
from config import Config  # Import the Config class

form_bp = Blueprint('form', __name__)

def get_db_connection():
    connection = psycopg2.connect(Config.DATABASE_URL)
    return connection

# Function to create the favorite article table if it doesn't exist
def create_add_fav():
    connection = get_db_connection()
    cursor = connection.cursor()
    # Create the favorite article table referencing news.id
    cursor.execute('''CREATE TABLE IF NOT EXISTS favArt (
                        id SERIAL PRIMARY KEY,
                        username TEXT NOT NULL,
                        news_id INTEGER NOT NULL,
                        FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE)''')
    connection.commit()
    connection.close()

# Call the function to initialize the database
create_add_fav()

# Handle GET request to retrieve favorite articles
@form_bp.route('/favorites/<username>', methods=['GET'])
def get_favorites_by_user(username):
    """Get all favorites for a specific user along with article details."""
    connection = get_db_connection()
    cursor = connection.cursor()
    # Query to get all favorite articles by joining the favArt table with the news table
    cursor.execute('''SELECT favArt.id, news.headline, news.summary, news.link
                      FROM favArt
                      JOIN news ON favArt.news_id = news.id
                      WHERE favArt.username = %s''', (username,))
    articles = cursor.fetchall()

    if articles:
        # Prepare the response with article details
        favorites_list = [{'id': article[0], 'headline': article[1], 'summary': article[2], 'link': article[3]} for article in articles]
        connection.close()
        return jsonify({'favorites': favorites_list}), 200
    else:
        connection.close()
        return jsonify({'error_message': 'No favorites found for this user'}), 404

# Handle POST request to add favorite articles
@form_bp.route('/addFavorites', methods=['POST'])
def add_favorite():
    data = request.get_json()
    username = data.get('username')
    news_id = data.get('news_id')

    if not username or not news_id:
        return {'error_message': 'Username and news_id are required'}, 400

    connection = get_db_connection()
    cursor = connection.cursor()
    # Check if the favorite already exists
    cursor.execute('SELECT * FROM favArt WHERE username = %s AND news_id = %s', (username, news_id))
    if cursor.fetchone():
        connection.close()
        return {'error_message': 'This article is already in your favorites'}, 400

    # Insert the new favorite into the favArt table
    cursor.execute('INSERT INTO favArt (username, news_id) VALUES (%s, %s)', (username, news_id))
    connection.commit()
    connection.close()

    return {'message': 'Favorite added successfully'}, 201

# Handle PUT request to edit the headline of an article
@form_bp.route('/editHeadline', methods=['PUT'])
def edit_headline():
    data = request.get_json()
    old_headline = data.get('old_headline')
    new_headline = data.get('new_headline')

    if not old_headline or not new_headline:
        return {'error_message': 'Old headline and new headline are required'}, 400

    connection = get_db_connection()
    cursor = connection.cursor()
    # Update the headline in the news table
    cursor.execute('''UPDATE news
                      SET headline = %s
                      WHERE headline = %s''', (new_headline, old_headline))
    if cursor.rowcount == 0:
        connection.close()
        return {'error_message': 'No favorites found for the given headline'}, 404

    connection.commit()
    connection.close()

    return {'message': 'Headline updated successfully'}, 200

# Handle DELETE request to remove a favorite article
@form_bp.route('/deleteFavorite/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    # Delete the favorite from the favArt table
    cursor.execute('DELETE FROM favArt WHERE id = %s', (id,))
    if cursor.rowcount == 0:
        connection.close()
        return jsonify({'error_message': 'Favorite not found'}), 404

    connection.commit()
    connection.close()
    return jsonify({'message': 'Favorite deleted successfully'}), 200
