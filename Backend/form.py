from flask import Blueprint, request, jsonify
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

form_bp = Blueprint('form', __name__)

# Function to create the favorite article table if it doesn't exist
def create_add_fav():
    try:
        with sqlite3.connect('news.db') as connection:
            cursor = connection.cursor()
            # Create the favorite article table referencing news.id
            cursor.execute('''CREATE TABLE IF NOT EXISTS favArt (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                news_id INTEGER NOT NULL,
                                FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE)''')
            connection.commit()
            logger.debug('Favorite article table created or already exists.')
    except sqlite3.Error as e:
        logger.error(f'Error creating favorite article table: {e}')

# Call the function to initialize the database
create_add_fav()

# Handle GET request to retrieve favorite articles
@form_bp.route('/favorites/<username>', methods=['GET'])
def get_favorites_by_user(username):
    """Get all favorites for a specific user along with article details."""
    logger.debug(f'Retrieving favorites for user: {username}')
    try:
        with sqlite3.connect('news.db') as connection:
            cursor = connection.cursor()
            # Query to get all favorite articles by joining the favArt table with the news table
            cursor.execute('''SELECT favArt.id, news.headline, news.summary, news.link
                              FROM favArt
                              JOIN news ON favArt.news_id = news.id
                              WHERE favArt.username = ?''', (username,))
            articles = cursor.fetchall()

            if articles:
                # Prepare the response with article details
                favorites_list = [{'id': article[0], 'headline': article[1], 'summary': article[2], 'link': article[3]} for article in articles]
                logger.debug(f'Found {len(favorites_list)} favorite articles for user: {username}')
                return jsonify({'favorites': favorites_list}), 200
            else:
                logger.debug(f'No favorites found for user: {username}')
                return jsonify({'error_message': 'No favorites found for this user'}), 404
    except sqlite3.Error as e:
        logger.error(f'Error retrieving favorites for user {username}: {e}')
        return jsonify({'error_message': 'Internal server error'}), 500

# Handle POST request to add favorite articles
@form_bp.route('/addFavorites', methods=['POST'])
def add_favorite():
    data = request.get_json()
    username = data.get('username')
    news_id = data.get('news_id')

    if not username or not news_id:
        logger.debug('Username and news_id are required.')
        return {'error_message': 'Username and news_id are required'}, 400

    try:
        with sqlite3.connect('news.db') as connection:
            cursor = connection.cursor()
            # Check if the favorite already exists
            cursor.execute('SELECT * FROM favArt WHERE username = ? AND news_id = ?', (username, news_id))
            if cursor.fetchone():
                logger.debug(f'Article with news_id {news_id} is already in favorites for user: {username}')
                return {'error_message': 'This article is already in your favorites'}, 400

            # Insert the new favorite into the favArt table
            cursor.execute('INSERT INTO favArt (username, news_id) VALUES (?, ?)', (username, news_id))
            connection.commit()
            logger.debug(f'Favorite added for user: {username}, news_id: {news_id}')
    except sqlite3.Error as e:
        logger.error(f'Error adding favorite for user {username}, news_id {news_id}: {e}')
        return jsonify({'error_message': 'Internal server error'}), 500

    return {'message': 'Favorite added successfully'}, 201

# Handle PUT request to edit the headline of an article
@form_bp.route('/editHeadline', methods=['PUT'])
def edit_headline():
    data = request.get_json()
    old_headline = data.get('old_headline')
    new_headline = data.get('new_headline')

    if not old_headline or not new_headline:
        logger.debug('Old headline and new headline are required.')
        return {'error_message': 'Old headline and new headline are required'}, 400

    try:
        with sqlite3.connect('news.db') as connection:
            cursor = connection.cursor()
            # Update the headline in the news table
            cursor.execute('''UPDATE news
                              SET headline = ?
                              WHERE headline = ?''', (new_headline, old_headline))
            if cursor.rowcount == 0:
                logger.debug(f'No articles found with the headline: {old_headline}')
                return {'error_message': 'No favorites found for the given headline'}, 404

            connection.commit()
            logger.debug(f'Headline updated from {old_headline} to {new_headline}')
    except sqlite3.Error as e:
        logger.error(f'Error updating headline from {old_headline} to {new_headline}: {e}')
        return jsonify({'error_message': 'Internal server error'}), 500

    return {'message': 'Headline updated successfully'}, 200

# Handle DELETE request to remove a favorite article
@form_bp.route('/deleteFavorite/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    logger.debug(f'Deleting favorite with id: {id}')
    try:
        with sqlite3.connect('news.db') as connection:
            cursor = connection.cursor()
            # Delete the favorite from the favArt table
            cursor.execute('DELETE FROM favArt WHERE id = ?', (id,))
            if cursor.rowcount == 0:
                logger.debug(f'Favorite with id {id} not found.')
                return jsonify({'error_message': 'Favorite not found'}), 404

            connection.commit()
            logger.debug(f'Favorite with id {id} deleted successfully.')
    except sqlite3.Error as e:
        logger.error(f'Error deleting favorite with id {id}: {e}')
        return jsonify({'error_message': 'Internal server error'}), 500

    return jsonify({'message': 'Favorite deleted successfully'}), 200
