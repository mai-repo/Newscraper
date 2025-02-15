import unittest
import sqlite3
from flask import Flask
from pokemon import pokemon
from unittest.mock import patch, MagicMock

class TestPokemonAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.register_blueprint(pokemon)
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

        # Setup test database
        with sqlite3.connect('news.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS pokemon")
            cursor.execute('''CREATE TABLE pokemon (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              username TEXT NOT NULL,
                              pokemonName TEXT NOT NULL,
                              image TEXT NOT NULL)''')
            conn.commit()

    def tearDown(self):
        """Clean up after each test."""
        with sqlite3.connect('news.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pokemon")
            conn.commit()

    @patch('requests.get')
    def test_get_Pokemon_success(self, mock_get):
        """Test getting Pokemon details successfully."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'pikachu',
            'sprites': {'front_default': 'http://example.com/pikachu.png'}
        }
        mock_get.return_value = mock_response

        response = self.client.get('/catchEm?name=pikachu')
        print("test_get_Pokemon_success response:", response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'pokemonName': 'pikachu',
            'image': 'http://example.com/pikachu.png'
        })

    @patch('requests.get')
    def test_get_Pokemon_not_found(self, mock_get):
        """Test getting Pokemon details when Pokemon is not found."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        response = self.client.get('/catchEm?name=unknown')
        print("test_get_Pokemon_not_found response:", response.json)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'Pokemon not found'})

    def test_save_Pokemon_success(self):
        """Test saving a Pokemon successfully."""
        payload = {
            'username': 'testuser',
            'pokemonName': 'pikachu',
            'image': 'http://example.com/pikachu.png'
        }
        response = self.client.post('/savePokemon', json=payload)
        print("test_save_Pokemon_success response:", response.json)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'message': 'Pokemon saved successfully'})

    def test_update_Pokemon_success(self):
        """Test updating a Pokemon successfully."""
        # First, save a Pokemon to update
        with sqlite3.connect('news.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pokemon (username, pokemonName, image) VALUES (?, ?, ?)",
                           ('testuser', 'pikachu', 'http://example.com/pikachu.png'))
            pokemon_id = cursor.lastrowid
            conn.commit()

        payload = {
            'username': 'updateduser',
            'pokemonName': 'raichu',
            'image': 'http://example.com/raichu.png'
        }
        response = self.client.put(f'/updatePokemon/{pokemon_id}', json=payload)
        print("test_update_Pokemon_success response:", response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Pokemon updated successfully'})

    def test_update_Pokemon_missing_data(self):
        """Test updating a Pokemon with missing data."""
        payload = {
            'username': 'updateduser',
            'pokemonName': 'raichu'
            # Missing 'image'
        }
        response = self.client.put('/updatePokemon/1', json=payload)
        print("test_update_Pokemon_missing_data response:", response.json)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Missing data'})

    def test_delete_Pokemon_success(self):
        """Test deleting a Pokemon successfully."""
        # First, save a Pokemon to delete
        with sqlite3.connect('news.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pokemon (username, pokemonName, image) VALUES (?, ?, ?)",
                           ('testuser', 'pikachu', 'http://example.com/pikachu.png'))
            pokemon_id = cursor.lastrowid
            conn.commit()

        response = self.client.delete(f'/deletePokemon/{pokemon_id}')
        print("test_delete_Pokemon_success response:", response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Pokemon deleted successfully'})

    def test_get_all_Pokemon(self):
        """Test getting all Pokemon from the database."""
        # First, save a Pokemon to retrieve
        with sqlite3.connect('news.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pokemon (username, pokemonName, image) VALUES (?, ?, ?)",
                           ('testuser', 'pikachu', 'http://example.com/pikachu.png'))
            conn.commit()

        response = self.client.get('/getPokemon')
        print("test_get_all_Pokemon response:", response.json)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['pokemonName'], 'pikachu')

    def test_change_profile_photo_success(self):
        """Test changing the profile photo of a Pokemon successfully."""
        # First, save a Pokemon to update
        with sqlite3.connect('news.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pokemon (username, pokemonName, image) VALUES (?, ?, ?)",
                           ('testuser', 'pikachu', 'http://example.com/pikachu.png'))
            pokemon_id = cursor.lastrowid
            conn.commit()

        payload = {
            'pokemon_id': pokemon_id,
            'image': 'http://example.com/raichu.png'
        }
        response = self.client.put('/changeProfile', json=payload)
        print("test_change_profile_photo_success response:", response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Profile photo updated successfully'})

    def test_change_profile_photo_not_found(self):
        """Test changing the profile photo of a non-existent Pokemon."""
        payload = {
            'pokemon_id': 999,
            'image': 'http://example.com/raichu.png'
        }
        response = self.client.put('/changeProfile', json=payload)
        print("test_change_profile_photo_not_found response:", response.json)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'Pokemon not found'})

if __name__ == '__main__':
    unittest.main()
