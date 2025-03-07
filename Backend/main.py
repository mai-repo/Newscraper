from flask import Flask, render_template, request, jsonify, send_from_directory
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# from redis import Redis
from bs4 import BeautifulSoup
import sqlite3
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from flask_cors import CORS
from form import form_bp
from pokemon import pokemon
import logging
import requests

# Load environment variables from .env file
load_dotenv()

# Google key and environment variables
GOOGLE_CLIENT_KEY = os.getenv("GOOGLE_CLIENT_KEY")
RECAPTCHA_SECRET_KEY = os.getenv("BACKEND_KEY")
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Function to initialize the database by creating the 'news' table if it doesn't exist
def setup_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect('news.db')
    cursor = connection.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS news (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        headline TEXT NOT NULL,
                        summary TEXT NOT NULL,
                        link TEXT NOT NULL)''')

    # Create the FTS5 virtual table for full-text search
    cursor.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS news_fts USING fts5(
                        id, headline, summary, link)''')

    # Trigger to keep the FTS5 table in sync with the news table
    cursor.execute('''CREATE TRIGGER IF NOT EXISTS news_ai AFTER INSERT ON news
                      BEGIN
                          INSERT INTO news_fts(rowid, id, headline, summary, link)
                          VALUES (new.id, new.id, new.headline, new.summary, new.link);
                      END;''')

    cursor.execute('''CREATE TRIGGER IF NOT EXISTS news_ad AFTER DELETE ON news
                      BEGIN
                          DELETE FROM news_fts WHERE id = old.id;
                      END;''')

    cursor.execute('''CREATE TRIGGER IF NOT EXISTS news_au AFTER UPDATE ON news
                      BEGIN
                          UPDATE news_fts SET headline = new.headline, summary = new.summary, link = new.link
                          WHERE id = old.id;
                      END;''')

    connection.commit()
    connection.close()

# Call the function to initialize the database
setup_database()


# Initialize the Flask application
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "https://mai-newscraper.vercel.app"}})

# # Configure Flask-Limiter to use Redis
# limiter = Limiter(
#     get_remote_address,
#     app=app,
#     storage_uri="redis://127.0.0.1:6379",  # Use Redis as the storage backend
#     default_limits=["50 per 3 minutes"],
# )

# Register the Blueprint
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

        # Insert scraped data into SQLite database
        connection = sqlite3.connect('news.db')
        cursor = connection.cursor()

        # Insert headlines and descriptions into the news table
        for headline, summary, link in zip(headlines_text, summaries_text, links_text):
            cursor.execute("INSERT INTO news (headline, summary, link) VALUES (?, ?, ?)",
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

        # Connect to the SQLite database
        connection = sqlite3.connect('news.db')
        cursor = connection.cursor()

        # Select all rows from the 'news' table
        cursor.execute("SELECT COUNT(*) FROM news")
        total_articles = cursor.fetchone()[0]

        total_pages = (total_articles + per_page - 1) // per_page

        # Fetch the paginated results
        start = (page - 1) * per_page
        cursor.execute("SELECT * FROM news LIMIT ? OFFSET ?", (per_page, start))
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
    Fetches all headlines from the 'news' table in the SQLite database
    that match the specified keywords and returns them as a JSON response.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect('news.db')
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

#complex search
@app.route('/search', methods=['GET'])
def search_articles():
    try:
        # Get the search query for headline and summary from request args
        headline_query = request.args.get('headline_query', '', type=str)
        summary_query = request.args.get('summary_query', '', type=str)

        # Connect to the SQLite database
        connection = sqlite3.connect('news.db')
        cursor = connection.cursor()

        # Perform full-text search on the 'news_fts' virtual table for both headline and summary
        cursor.execute('''SELECT id, headline, summary, link FROM news_fts
                          WHERE headline MATCH ? OR summary MATCH ?''', (headline_query, summary_query))
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
        secret = RECAPTCHA_SECRET_KEY

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
        id_token.verify_oauth2_token(token, Request(), GOOGLE_CLIENT_KEY), 200

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
    app.run(debug=True, port=5000)
