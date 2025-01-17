# News Scraper Application

This **Flask**-based application scrapes the latest news headlines and descriptions from **BBC News** and stores the data on **Firebase**.

## Table of Contents

- [News Scraper Application](#news-scraper-application)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Setup Instructions](#setup-instructions)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Create a virtual environment](#2-create-a-virtual-environment)
    - [3. Create a .gitignore](#3-create-a-gitignore)
    - [4. Install Dependencies](#4-install-dependencies)
    - [5. Setup Firebase](#5-setup-firebase)
    - [6. Run the Flask Application](#6-run-the-flask-application)

## Requirements

The following Python packages are required to run the application:
- **Flask**: Web framework for Python.
- **requests**: HTTP library for sending GET requests to fetch the news data.
- **beautifulsoup4**: Library for parsing HTML and scraping data.
- **firebase-admin**: Firebase Admin SDK to interact with Firebase Firestore.

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
### 5. Setup Firebase

- Create a Firebase project at Firebase Console.
- Download your Firebase service account key file and save it (e.g. newsKey.json).
- Place the account file in the root directory of your project and add it to your `.gitignore`.

### 6. Run the Flask Application
```bash
export FLASK_APP=main.py
flask run
```