from flask import Flask, request

# Initialize the Flask application
# This creates an instance of the Flask class and assigns it to the variable app.
app = Flask(__name__)

@app.route("/")  # Define the route for the root URL
def index():
    return "Drink more coffee RIGHT NOW!!"

if __name__ == '__main__':
    app.run(port=5000)
