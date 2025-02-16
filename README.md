# News Scraper Application

This **Flask**-based application scrapes the latest news headlines and descriptions from the **Atlantic** and stores the data before rendering it on a webpage. Additionally, it integrates with the Pokémon API to fetch and manage Pokémon data.

## Table of Contents
- [News Scraper Application](#news-scraper-application)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Setup Instructions](#setup-instructions)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Create a virtual environment](#2-create-a-virtual-environment)
    - [3. Create a .gitignore](#3-create-a-gitignore)
    - [4. Install Dependencies](#4-install-dependencies)
    - [5. Set Up Google Applications and Keys](#5-set-up-google-applications-and-keys)
    - [Google Application Setup and .env Configuration](#google-application-setup-and-env-configuration)
      - [1. Create a Google Cloud Project](#1-create-a-google-cloud-project)
      - [2. Create OAuth 2.0 Credentials](#2-create-oauth-20-credentials)
      - [3. Set Up reCAPTCHA](#3-set-up-recaptcha)
      - [4. Create `.env` File](#4-create-env-file)
    - [6. Data Schema](#6-data-schema)
        - [News Data Schema](#news-data-schema)
        - [Pokémon Data Schema](#pokémon-data-schema)
        - [Favorite Articles Data Schema](#favorite-articles-data-schema)
    - [7. Download Frontend Dependencies](#7-download-frontend-dependencies)
    - [8. Run the Flask Application](#8-run-the-flask-application)
    - [9. Open your web browser](#9-open-your-web-browser)
- [Testing Instructions](#testing-instructions)
  - [1. Set Up the Testing Environment](#1-set-up-the-testing-environment)
    - [Using unittest](#using-unittest)
  - [2. View Test Coverage Report](#2-view-test-coverage-report)
    - [Install pytest-cov](#install-pytest-cov)
    - [Run Tests with Coverage](#run-tests-with-coverage)
  - [Stretch Goals](#stretch-goals)

## Requirements

The following Python packages are required to run the application:
- **Flask**: Web framework for Python.
- **requests**: HTTP library for sending GET requests to fetch the news data.
- **beautifulsoup4**: Library for parsing HTML and scraping data.
- **google-auth**: Library for authenticating with Google services.
- **google-auth-oauthlib**: Library for OAuth 2.0 authentication with Google.
- **Svelte**: A modern JavaScript framework for building user interfaces.

## Setup Instructions

Follow these steps to get the application up and running:

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/mai-repo/RG-Knowledge-Check-1.git
```
### 2. Create a virtual environment

```bash
python -m venv .venv
```
### 3. Create a .gitignore
- Add .venv in the `.gitignore` file

### 4. Install Dependencies
- Install all the required Python packages

```bash
pip3 install -r requirements.txt
```

### 5. Set Up Google Applications and Keys
- Follow the instructions to set up Google applications and obtain the necessary keys for authentication.

### Google Application Setup and .env Configuration

#### 1. Create a Google Cloud Project
- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project and enable the following APIs:
  - Google Identity Services API
  - reCAPTCHA API

#### 2. Create OAuth 2.0 Credentials
- Go to **Credentials** in the Google Cloud Console.
- Create **OAuth 2.0 Client ID** for a web app.
- Add authorized origins (e.g., `http://127.0.0.1:5000/`).
- Download the JSON file with client secrets.

#### 3. Set Up reCAPTCHA
- Register your site in the [reCAPTCHA Admin Console](https://www.google.com/recaptcha/admin).
- Choose reCAPTCHA type (v2).
- Obtain **site key** and **secret key**.

#### 4. Create `.env` File
- Create a `.env` file in the root directory of your project.
- Add the following variables:

```env
GOOGLE_CLIENT_SECRET=your-google-client-secret
RECAPTCHA_SECRET_KEY=your-recaptcha-secret-key

```

### 6. Data Schema
##### News Data Schema
  - The news data is stored in an SQLite database with the following schema:
```sql
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    headline TEXT NOT NULL,
    summary TEXT NOT NULL,
    link TEXT NOT NULL
);
```

##### Pokémon Data Schema
- The Pokémon data is stored in an SQLite database with the following schema:
```sql
CREATE TABLE IF NOT EXISTS pokemon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    pokemonName TEXT NOT NULL,
    image TEXT NOT NULL
);
```

##### Favorite Articles Data Schema
- The favorite articles data is stored in an SQLite database with the following schema:
```sql
  CREATE TABLE IF NOT EXISTS favArt (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT NOT NULL,
      news_id INTEGER NOT NULL,
      FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE)
);
```

### 7. Download Frontend Dependencies
- Navigate to the frontend directory:
  `cd Frontend`
- Install Dependencies:
  `npm install `

### 8. Run the Flask Application

```bash
export FLASK_APP=main.py
flask run
```
### 9. Open your web browser
![A webpage with a webscraper that asks user to click a button to scrape data from the Atlantic and returns a JSON file with the latest headlines](https://i.imgflip.com/9iamed.gif)

# Testing Instructions

Follow these steps to run the tests for the application:

## 1. Set Up the Testing Environment
Ensure that you have installed all the required dependencies as mentioned in the **Setup Instructions**.

### Using unittest
To run tests with `unittest`, use the following command:

```bash
python -m unittest discover -s Backend/tests -p "test_*.py"
```

## 2. View Test Coverage Report
If you want to generate a test coverage report, you can use `pytest-cov`.

### Install pytest-cov
Install `pytest-cov` using the following command:

```bash
pip install pytest-cov
```

### Run Tests with Coverage
Run the tests with coverage using the following command:

```bash
pytest --cov=Backend --cov-report=html Backend/tests
```

This will generate a coverage report in the `htmlcov` directory. You can view the report by opening the `index.html` file in a web browser:

```bash
open htmlcov/index.html
```


## Stretch Goals
- Allow users to choose from a variety of news sites