import unittest
import sqlite3
from flask import Flask
from form import form_bp

class TestFavoritesArticles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.register_blueprint(form_bp)
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

        # Setup test database
        with sqlite3.connect('news.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS favArt")
            cursor.execute("DROP TABLE IF EXISTS news")
            cursor.execute('''CREATE TABLE news (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              headline TEXT NOT NULL,
                              summary TEXT NOT NULL,
                              link TEXT NOT NULL)''')
            cursor.execute('''CREATE TABLE favArt (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              username TEXT NOT NULL,
                              news_id INTEGER NOT NULL,
                              FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE)''')
            cursor.execute("INSERT INTO news (headline, summary, link) VALUES (?, ?, ?)",
                           ("Sample Headline", "Sample Summary", "http://example.com"))
            conn.commit()

    def test_add_favorite_success(self):
        #Test for a successful favorite addition
        payload = {'username': 'testuser', 'news_id': 1}
        response = self.client.post('/addFavorites', json=payload)
        print("test_add_favorite_success response:", response.json)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'message': 'Favorite added successfully'})

    def test_get_favorite_article_by_user_not_found(self):
        response = self.client.get('/favorites/kim')
        print("test_get_favorite_article_by_user_not_found response:", response.json)
        self.assertEqual(response.status_code, 404)

    def test_edit_headline(self):
        #Test editing the headline of an existing news article.
        response = self.client.put('/editHeadline', json={'old_headline': 'Sample Headline', 'new_headline': 'Updated Headline'})
        print("test_edit_headline response:", response.json)
        self.assertEqual(response.status_code, 200)

    def test_edit_headline_not_found(self):
        #Test editing the headline of a non-existent news article.
        response = self.client.put('/editHeadline', json={'old_headline': 'Nonexistent Headline', 'new_headline': 'Updated Headline'})
        print("test_edit_headline_not_found response:", response.json)
        self.assertEqual(response.status_code, 404)

    def test_delete_favorite_article(self):
        #Test deleting a favorite article by its ID.
        response = self.client.delete('/deleteFavorite/1')
        print("test_delete_favorite_article response:", response.json)
        self.assertEqual(response.status_code, 200)

    def test_delete_favorite_article_not_found(self):
        #Test deleting a non-existent favorite article by its ID.
        response = self.client.delete('/deleteFavorite/999')
        print("test_delete_favorite_article_not_found response:", response.json)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
