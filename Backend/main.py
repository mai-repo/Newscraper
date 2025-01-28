from flask import Flask, render_template, request, jsonify
import requests
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis
from bs4 import BeautifulSoup
import sqlite3
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2 import id_token

#Google key and environment variables
GOOGLE_CLIENT_KEY= os.getenv("GOOGLE_CLIENT_KEY")
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"

# Load environment variables from .env file
load_dotenv()

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

    connection.commit()
    connection.close()

# Call the function to initialize the database
setup_database()

# Initialize the Flask application
app = Flask(__name__, template_folder='/Users/thanhmai/Documents/RG-Knowledge-Check-1/templates')

# Configure Flask-Limiter to use Redis
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="redis://127.0.0.1:6379",  # Use Redis as the storage backend
    default_limits=["50 per 30 minutes"],
)

# Define a custom error handler for rate limit errors (HTTP 429)
@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify(error="ratelimit exceeded", message="Too many requests, please try again later."), 429

@app.route("/")  # Define the route for the root URL
def index():
    # Render the template
    return render_template("index.html")

@app.route("/scrape_page")  # Define the route for the scrape page URL
def scrape_page():
    # Render the scrape template
    return render_template("scrape.html")

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

        return jsonify({"message": "News added successfully!"}), 201

    except requests.exceptions.RequestException as e:
        # Handle request-related errors
        return f"Error fetching the page: {e}"

    except Exception as e:
        # Handle other types of exceptions
        return f"An error occurred: {e}"

@app.route("/headlines")
def get_headlines():
    """
    Fetches all headlines from the 'news' table in the SQLite database
    and returns them as a JSON response.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect('news.db')
        cursor = connection.cursor()

        # Execute SQL query to fetch all headlines from the 'news' table
        cursor.execute("SELECT headline FROM news")
        rows = cursor.fetchall()

        # Prepare a list of dictionaries, each containing the id and headline
        headlines_data = [{'headline': row[0]} for row in rows]

        # Close the database connection
        connection.close()

        # Return the fetched headlines as a JSON response
        return jsonify(headlines_data)

    except Exception as e:
        # Return an error message if an exception occurs
        return f"Error occurred while fetching headlines: {e}"


@app.route("/summaries")
def get_summaries():
    """
    Fetches all summaries from the 'news' table in the SQLite database
    and returns them as a JSON response.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect('news.db')
        cursor = connection.cursor()

        # Execute SQL query to fetch all summaries from the 'news' table
        cursor.execute("SELECT summary FROM news")
        rows = cursor.fetchall()

        # Prepare a list of dictionaries, each containing the summary
        summaries_data = [{'summary': row[0]} for row in rows]

        # Close the database connection
        connection.close()

        # Return the fetched summaries as a JSON response
        return jsonify(summaries_data)

    except Exception as e:
        # Return an error message if an exception occurs
        return f"Error occurred while fetching summaries: {e}"

@app.route('/verifyUser', methods=['POST'])
@limiter.limit("5 per 5 mins")
def verify_user():
    try:
        data = request.get_json()  # Correctly get JSON data from the request
        token = data.get('token')
        secret = os.getenv("BACKEND_KEY")

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
            return jsonify(message='reCAPTCHA verified successfully!')
        else:
            return jsonify(message='Failed to verify reCAPTCHA.'), 400
    except Exception as e:
        return jsonify(message=str(e)), 500

#Function to handle User Sign-In with Google
@app.route('/userSignIn', methods=['POST'])
def userSignIn():
    token = request.json.get('token')
    if not token:
        return jsonify(message="No token provided"), 400
    try:
        id_token.verify_oauth2_token(token, Request(), GOOGLE_CLIENT_KEY)

        return jsonify(message='Google Sign-In successful!')

    except Exception as e:
        return jsonify(message="Invalid token", error=str(e)), 400

if __name__ == '__main__':
    # Run the Flask app in debug mode on port 5000
    app.run(debug=True, port=5000)
