from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import sqlite3
from flask_tailwind import Tailwind

# Function to initialize the database by creating the 'news' table if it doesn't exist
def setup_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect('news.db')
    cursor = connection.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS news (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        headline TEXT NOT NULL,
                        description TEXT NOT NULL)''')

    connection.commit()
    connection.close()


# Call the function to initialize the database
setup_database()

# Initialize the Flask application
app = Flask(__name__)

# Initialize Tailwind CSS
tailwind = Tailwind(app)

@app.route("/")  # Define the route for the root URL
def index():
    # Render the template
    return render_template("index.html")


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

        # Grab descriptions
        descriptions = soup.find_all(
            'p', attrs={'data-testid': 'card-description'})
        descriptions_text = [desc.get_text() for desc in descriptions]

        # Insert scraped data into SQLite database
        connection = sqlite3.connect('news.db')
        cursor = connection.cursor()

        # Insert headlines and descriptions into the news table
        for headline, description in zip(headlines_text, descriptions_text):
            cursor.execute("INSERT INTO news (headline, description) VALUES (?, ?)",
                    (headline, description))

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


if __name__ == '__main__':
    # Run the Flask app in debug mode on port 5000
    app.run(debug=True, port=5000)
