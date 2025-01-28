# News Scraper Application

This **Flask**-based application scrapes the latest news headlines and descriptions from the **Atlantic** and stores the data before rendering it on a webpage.

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
    - [7. Open your web browser](#7-open-your-web-browser)
  - [Stretch Goals](#stretch-goals)

## Requirements

The following Python packages are required to run the application:
- **Flask**: Web framework for Python.
- **requests**: HTTP library for sending GET requests to fetch the news data.
- **beautifulsoup4**: Library for parsing HTML and scraping data.
- **google-auth**: Library for authenticating with Google services.
- **google-auth-oauthlib**: Library for OAuth 2.0 authentication with Google.

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

markdown
Copy
Edit
# Google Application Setup and .env Configuration

## 1. Create a Google Cloud Project
- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project and enable the following APIs:
  - Google Identity Services API
  - reCAPTCHA API

## 2. Create OAuth 2.0 Credentials
- Go to **Credentials** in the Google Cloud Console.
- Create **OAuth 2.0 Client ID** for a web app.
- Add authorized origins (e.g., `http://127.0.0.1:5000/`).
- Download the JSON file with client secrets.

## 3. Set Up reCAPTCHA
- Register your site in the [reCAPTCHA Admin Console](https://www.google.com/recaptcha/admin).
- Choose reCAPTCHA type (v2).
- Obtain **site key** and **secret key**.

## 4. Create `.env` File
- Create a `.env` file in the root directory of your project.
- Add the following variables:

```env
GOOGLE_CLIENT_SECRET=your-google-client-secret
RECAPTCHA_SECRET_KEY=your-recaptcha-secret-key

### 6. Run the Flask Application
```bash
export FLASK_APP=main.py
flask run
```
### 7. Open your web browser

![A webpage with a webscraper that asks user to click a button to scrape data from the Atlantic and returns a JSON file with the latest headlines](https://i.imgflip.com/9iamed.gif)


## Stretch Goals
- Allow users to choose from a variety of news sites
- A music player to let user listen to music while browsing articles

