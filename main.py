from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import sqlite3

# Create news table


def init_db():
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
init_db()

# Initialize the Flask application
app = Flask(__name__)

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
        # Or adjust the tag/class as needed
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


if __name__ == '__main__':
    # Run the Flask app in debug mode on port 5000
    app.run(debug=True, port=5000)
