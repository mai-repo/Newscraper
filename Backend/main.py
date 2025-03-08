from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import psycopg2
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from flask_cors import CORS
from Backend.form import form_bp
from Backend.pokemon import pokemon
import logging
import requests
from Backend.config import Config

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize the Flask application
app = Flask(__name__)

# Load configuration settings
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "https://mai-newscraper.vercel.app"]}})

def get_db_connection():
    connection = psycopg2.connect(app.config["DATABASE_URL"])
    return connection

# Function to initialize the database by creating the 'news' table if it doesn't exist
def setup_database():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS news (
                        id SERIAL PRIMARY KEY,
                        headline TEXT NOT NULL,
                        summary TEXT NOT NULL,
                        link TEXT NOT NULL)''')

    # Create the full-text search table (optional)
    cursor.execute('''CREATE EXTENSION IF NOT EXISTS pg_trgm''')  # PostgreSQL text search extension
    cursor.execute('''CREATE TABLE IF NOT EXISTS news_fts (
                        id INT PRIMARY KEY,
                        headline TEXT,
                        summary TEXT,
                        link TEXT)''')

    cursor.execute('''CREATE INDEX IF NOT EXISTS headline_idx ON news_fts USING gin (headline gin_trgm_ops)''')
    cursor.execute('''CREATE INDEX IF NOT EXISTS summary_idx ON news_fts USING gin (summary gin_trgm_ops)''')

    connection.commit()
    connection.close()

# Call the function to initialize the database
setup_database()

# Register the Blueprints
app.register_blueprint(form_bp)
app.register_blueprint(pokemon)

@app.route("/")  # Define the route for the root URL
def index():
    return jsonify({'message': 'Welcome to the API!'})

@app.route("/scrape")
def scrape():
    try:
        # Send GET request to fetch the page content
        response = requests.get('https://www.theatlantic.com/most-popular/')
        response.raise_for_status()  # Ensure the request was successful

        # Parse the HTML document
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all('article')
        headlines_text = []
        summaries_text = []
        links_text = []

        for article in articles:
            # Find the h2 tag (headline) within the article
            headline = article.select_one('h2')
            if headline:
                headlines_text.append(headline.get_text())

            # Find the p tag (summary) within the article
            summary = article.select_one('p')
            if summary:
                summaries_text.append(summary.get_text())

            # Find the link (<a> tag) within the article
            link = article.select_one('a')
            if link and link.get('href'):
                links_text.append(link['href'])

        # Ensure lists are aligned (handle missing summaries/links)
        summaries_text += [""] * (len(headlines_text) - len(summaries_text))
        links_text += [""] * (len(headlines_text) - len(links_text))

        # Insert scraped data into PostgreSQL database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert headlines and descriptions into the news table
        for headline, summary, link in zip(headlines_text, summaries_text, links_text):
            cursor.execute("INSERT INTO news (headline, summary, link) VALUES (%s, %s, %s)",
                (headline, summary, link))

        connection.commit()
        connection.close()

        articles_data = []
        for headline, summary, link in zip(headlines_text, summaries_text, links_text):
            articles_data.append({
            "headline": headline,
            "summary": summary,
            "link": link
            })

        return jsonify(articles_data), 201

    except Exception as e:
        logging.error(f"Error occurred during scraping: {e}")
        return render_template("error.html", error_message=f"An error occurred: {e}"), 500

@app.route('/news', methods=['GET'])
def get_news():
    try:
        # Get pagination parameters from request args,
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Connect to the PostgreSQL database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Select all rows from the 'news' table
        cursor.execute("SELECT COUNT(*) FROM news")
        total_articles = cursor.fetchone()[0]

        total_pages = (total_articles + per_page - 1) // per_page

        # Fetch the paginated results
        start = (page - 1) * per_page
        cursor.execute("SELECT * FROM news LIMIT %s OFFSET %s", (per_page, start))
        articles = cursor.fetchall()

        # Close the connection to the database
        connection.close()

        # Format the data into a list of dictionaries for JSON response
        articles_data = [{"id": article[0], "headline": article[1], "summary": article[2], "link": article[3]} for article in articles]

        return jsonify({
            "current_page": page,
            "total_pages": total_pages,
            "per_page": per_page,
            "total_articles": total_articles,
            "articles": articles_data
        }), 200

    except Exception as e:
        logging.error(f"Error occurred while fetching news: {e}")
        return render_template("error.html", error_message=f"Error occurred while fetching news: {e}"), 500

@app.route("/headlines")
def get_headlines():
    """
    Fetches all headlines from the 'news' table in the PostgreSQL database
    that match the specified keywords and returns them as a JSON response.
    """
    try:
        # Connect to the PostgreSQL database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Define the keywords to filter headlines
        keywords = ["Trump", "America", "DOGE"]

        # Prepare the SQL query to fetch headlines containing the keywords
        query = f"SELECT headline FROM news WHERE headline LIKE '%{keywords[0]}%' OR headline LIKE '%{keywords[1]}%' OR headline LIKE '%{keywords[2]}%'"

        # Execute the SQL query
        cursor.execute(query)
        rows = cursor.fetchall()

        # Prepare a list of dictionaries, each containing the headline
        headlines_data = [{'headline': row[0]} for row in rows]

        # Close the database connection
        connection.close()

        # Return the fetched headlines as a JSON response
        return jsonify(headlines_data), 200
    except Exception as e:
        logging.error(f"Error occurred while fetching summaries: {e}")
        return render_template("error.html", error_message=f"Error occurred while fetching summaries: {e}"), 500

# Complex search
@app.route('/search', methods=['GET'])
def search_articles():
    try:
        # Get the search query for headline and summary from request args
        headline_query = request.args.get('headline_query', '', type=str)
        summary_query = request.args.get('summary_query', '', type=str)

        # Connect to the PostgreSQL database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Perform full-text search on the 'news' table for both headline and summary
        cursor.execute('''SELECT id, headline, summary, link FROM news
                          WHERE headline LIKE %s OR summary LIKE %s''', (f'%{headline_query}%', f'%{summary_query}%'))
        articles = cursor.fetchall()

        # Close the connection to the database
        connection.close()

        # Format the data into a list of dictionaries for JSON response
        articles_data = [{"id": article[0], "headline": article[1], "summary": article[2], "link": article[3]} for article in articles]

        return jsonify(articles_data), 200

    except Exception as e:
        logging.error(f"Error occurred during search: {e}")
        return render_template("error.html", error_message=f"Error occurred during search: {e}"), 500

@app.route('/verifyUser', methods=['POST'])
def verify_user():
    try:
        data = request.get_json()  # Correctly get JSON data from the request
        token = data.get('token')
        secret = app.config["BACKEND_KEY"]

        # Send the POST request to Google's reCAPTCHA verification endpoint
        recaptcha_response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': secret,
                'response': token
            }
        )
        result = recaptcha_response.json()

        if result.get('success'):
            return jsonify(message='reCAPTCHA verified successfully!'), 200
        else:
            return jsonify(message='Failed to verify reCAPTCHA.'), 400
    except Exception as e:
        logging.error(f"Error occurred during reCAPTCHA verification: {e}")
        return jsonify(error="Server issue cannot validate at this time!"), 500

# Function to handle User Sign-In with Google
@app.route('/userSignIn', methods=['POST'])
def userSignIn():
    token = request.json.get('token')
    if not token:
        return jsonify(message="No token provided"), 404
    try:
        id_token.verify_oauth2_token(token, Request(), app.config["GOOGLE_CLIENT_KEY"]), 200

        return jsonify(message='Google Sign-In successful!'), 200

    except Exception as e:
        logging.error(f"Error occurred during Google Sign-In: {e}")
        return render_template("error.html", error_message="Invalid token or no token provided", error=str(e)), 500

# Route to explicitly serve the 500 error page with a custom error message
@app.route("/500")
def serve_500_page():
    error_message = "Internal server error, please try again later."
    return render_template("500.html", error_message=error_message), 500

@app.route('/error')
def handle_exception(e):
    return render_template("error.html", error_message="An unexpected error occurred. Please try again later."), 500

# 404 Not Found Error handler
@app.errorhandler(404)
def not_found(e):
    logging.error(f"404 error: Page is not found")
    return render_template("404.html", error_message="Page not found"), 404

# 500 Internal Server Error handler
@app.errorhandler(500)
def internal_server_error(e):
    logging.error(f"500 error: {e}")
    return render_template("500.html", error_message = "Internal server error, please try again later."), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Unexpected error: {e}")
    return render_template("error.html", error_message="An unexpected error occurred. Please try again later."), 500

if __name__ == '__main__':
    # Run the Flask app in debug mode on port 5000
    app.run(debug=True, port=9000)
