from flask import Flask, render_template, request, jsonify
import requests
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis
from bs4 import BeautifulSoup
import sqlite3
import os
from dotenv import load_dotenv

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
                        summary TEXT NOT NULL)''')

    connection.commit()
    connection.close()

# Call the function to initialize the database
setup_database()

# Initialize the Flask application
app = Flask(__name__)

# Configure Flask-Limiter to use Redis
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="redis://127.0.0.1:6379",  # Use Redis as the storage backend
    default_limits=["5 per 3 minutes"],
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
    return render_template("scrape.html", frontend_key=os.getenv("FRONTEND_KEY"))

@app.route("/scrape")
def scrape():
    try:
        # Send GET request to fetch the page content
        response = requests.get('https://www.bbc.com/news')
        response.raise_for_status()  # Ensure the request was successful

        # Parse the HTML document
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all h2 tags (headlines)
        headlines = soup.find_all('h2', attrs={'data-testid': 'card-headline'})
        headlines_text = [headline.get_text() for headline in headlines]

        # Grab summary
        summaries = soup.find_all('p')
        summaries_text = [summary.get_text() for summary in summaries]

        # Insert scraped data into SQLite database
        connection = sqlite3.connect('news.db')
        cursor = connection.cursor()

        # Insert headlines and descriptions into the news table
        for headline, summary in zip(headlines_text, summaries_text):
            cursor.execute("INSERT INTO news (headline, summary) VALUES (?, ?)",
                (headline, summary))

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

if __name__ == '__main__':
    # Run the Flask app in debug mode on port 5000
    app.run(debug=True, port=5000)
