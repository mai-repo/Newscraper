from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup

# Initialize the Flask application
# This creates an instance of the Flask class and assigns it to the variable app.
app = Flask(__name__)

# Define URLs for the websites to scrape
guardian_url = 'https://www.theguardian.com/us'
atlantic_url = 'https://www.theatlantic.com/'
vox_url = 'https://www.vox.com/'

@app.route("/")  # Define the route for the root URL
def index():
    # Render the template from the frontend folder
    return render_template("index.html")

@app.route("/scrape")
def scrape():
    try:
        # Send GET request to fetch the page content
        response = requests.get('https://www.bbc.com/news')
        response.raise_for_status()  # Ensure the request was successful

        # Parse the HTML document
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all h3 tags (headlines)
        headlines = soup.find_all('h2')
        headlines_text = [headline.get_text() for headline in headlines]
        print(headlines_text)

        # Return the headlines as a JSON response
        return jsonify(headlines_text)


    except requests.exceptions.RequestException as e:
        # Handle request-related errors
        return f"Error fetching the page: {e}"

    except Exception as e:
        # Handle other types of exceptions
        return f"An error occurred: {e}"

if __name__ == '__main__':
    # Run the Flask app in debug mode on port 5000
    app.run(debug=True, port=5000)
