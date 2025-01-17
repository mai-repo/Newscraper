from flask import Flask, request, render_template

# Initialize the Flask application
# This creates an instance of the Flask class and assigns it to the variable app.
app = Flask(__name__)


@app.route("/")  # Define the route for the root URL
def index():
    return render_template('index.html')


@app.route("/scrape") # Define the route to scrape
def scrape():
    return "Scraping in progress..."

if __name__ == '__main__':
    app.run(port=5000)
