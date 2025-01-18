# News Scraper Application

This **Flask**-based application scrapes the latest news headlines and descriptions from **BBC News** and stores the data before rendering it on a webpage.

## Table of Contents

- [News Scraper Application](#news-scraper-application)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Setup Instructions](#setup-instructions)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Create a virtual environment](#2-create-a-virtual-environment)
    - [3. Create a .gitignore](#3-create-a-gitignore)
    - [4. Install Dependencies](#4-install-dependencies)
    - [5. Run the Flask Application](#5-run-the-flask-application)
    - [6. Open your web browser](#6-open-your-web-browser)
    - [Stretch Goals](#stretch-goals)

## Requirements

The following Python packages are required to run the application:
- **Flask**: Web framework for Python.
- **requests**: HTTP library for sending GET requests to fetch the news data.
- **beautifulsoup4**: Library for parsing HTML and scraping data.

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

### 5. Run the Flask Application
```bash
export FLASK_APP=main.py
flask run
```
### 6. Open your web browser

![A webpage with a webscraper that asks user to click a button to scrape data from the BBC and returns a JSON file with the latest headlines](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTAxZDN3Y2FseXI4OTR2anp2NDZzM3h1a2ZlcWNoZGpwN3E0NmkzOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JTy9jAmhJyzBQHA0FG/giphy.gif)

### Stretch Goals
- Allow users to choose from a variety of news sites
- A music player to let user listen to music while browsing articles

