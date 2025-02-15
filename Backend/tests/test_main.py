import sqlite3
import unittest
from unittest.mock import patch, MagicMock
from main import app

class TestNewsApp(unittest.TestCase):

    def setUp(self):
        """Set up any state before the test cases run."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config["TESTING"] = True
        # Setup the database
        self.setup_database()

    def tearDown(self):
        """Clean up after all tests run."""
        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM news")
        conn.commit()
        conn.close()


    @patch("requests.get")  # Mock requests.get
    @patch("sqlite3.connect")  # Mock database connection
    def test_scrape_success(self, mock_connect, mock_get):
        """Test successful scraping and database insertion."""

        # Mock HTML response
        mock_html = """
        <html>
            <body>
                <article>
                    <h2>Example Headline</h2>
                    <p>Example Summary</p>
                    <a href="https://example.com/article1"></a>
                </article>
            </body>
        </html>
        """

        # Mock requests.get().content
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = mock_html
        mock_get.return_value = mock_response

        # Mock SQLite connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Send request to test endpoint
        response = self.client.get("/scrape")

        # Expected JSON output
        expected_output = [
            {
                "headline": "Example Headline",
                "summary": "Example Summary",
                "link": "https://example.com/article1",
            }
        ]

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), expected_output)

        # Verify database insertion was called
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()
        mock_conn.close.assert_called()

    @staticmethod
    def setup_database():
        """Initialize the database schema and insert test data."""
        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            headline TEXT,
                            summary TEXT,
                            link TEXT)''')
        conn.commit()
        conn.close()

    def test_insert_news(self):
        """Test inserting a news item into the database."""
        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO news(headline, summary, link) VALUES (?,?,?)",
                       ("Test Headline", "Test Summary", "http://test.com"))
        conn.commit()
        conn.close()

        response = self.client.get('/news')
        print("test_insert_news response:", response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['headline'], "Test Headline")
        self.assertEqual(response.json[0]['summary'], "Test Summary")
        self.assertEqual(response.json[0]['link'], "http://test.com")

    def test_index(self):
        response = self.client.get('/')
        print("test_index response:", response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Welcome to the API!'})

    def test_get_news_empty(self):
        response = self.client.get("/news")
        print("test_get_news_empty response:", response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    #Test that the /headlines endpoint
    def test_get_headlines(self):
        response = self.client.get('/headlines')
        print("test_get_headlines response:", response.json)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

# Run the tests
if __name__ == '__main__':
    unittest.main()