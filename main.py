from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize the Flask application
app = Flask(__name__)

cred = credentials.Certificate('newsKey.json')  # Path to the new key
firebase_admin.initialize_app(cred)
# Initialize Firestore
db = firestore.client()

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
        descriptions = soup.find_all('p', attrs={'data-testid': 'card-description'})  # Or adjust the tag/class as needed
        descriptions_text = [desc.get_text() for desc in descriptions]

        # Add the headlines to Firestore
        db.collection('News').add({
            'news': {
                'headlines': headlines_text,
                'descriptions': descriptions_text,
            }
        })
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
