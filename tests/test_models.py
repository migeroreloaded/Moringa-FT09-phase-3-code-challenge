import unittest
from unittest.mock import MagicMock
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def setUp(self):
        # Creating a mock for the database cursor
        self.cursor = MagicMock()

    def test_author_creation(self):
        # Testing Author creation
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        # Testing Article creation
        article = Article(1, "Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        # Testing Magazine creation
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")

    def test_create_author(self):
        # Testing author creation in the database
        self.cursor.lastrowid = 1  # Mocking the last inserted row ID
        self.cursor.execute.return_value = None  # Mocking the execute method to do nothing
        author_name = "John Doe"
        self.cursor.execute("INSERT INTO authors (name) VALUES (?)", (author_name,))
        author_id = self.cursor.lastrowid
        author = Author(id=author_id, name=author_name)
        self.assertEqual(author.name, "John Doe")
        self.assertEqual(author.id, 1)

    def test_get_all_authors(self):
        # Testing fetching all authors from the database
        self.cursor.fetchall.return_value = [(1, "John Doe"), (2, "Jane Smith")]
        authors = Author.get_all_authors(self.cursor)
        # Checking if execute method was called with correct argument
        self.cursor.execute.assert_called_once_with("SELECT * FROM authors")
        # Checking if authors were fetched correctly
        self.assertEqual(len(authors), 2)
        self.assertEqual(authors[0].id, 1)
        self.assertEqual(authors[0].name, "John Doe")
        self.assertEqual(authors[1].id, 2)
        self.assertEqual(authors[1].name, "Jane Smith")

    def test_author_articles(self):
        # Testing fetching articles by author
        articles_data = [(1, "Test Article", "Test Content", 1, 1)]  # Simulated articles data
        self.cursor.fetchall.return_value = articles_data
        author = Author(id=1, name="John Doe")
        articles = author.articles(self.cursor)
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0][0], 1)
        self.assertEqual(articles[0][1], "Test Article")

    def test_author_magazines(self):
        # Testing fetching magazines by author
        self.cursor.fetchall.return_value = [(1, "Tech Magazine", "Technology")]
        author = Author(1, "John Doe")
        magazines = author.magazines(self.cursor)
        # Checking if execute method was called with correct argument
        self.cursor.execute.assert_called_once_with("""
            SELECT DISTINCT magazines.*
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (1,))
        # Checking if magazines were fetched correctly
        self.assertEqual(len(magazines), 1)
        self.assertEqual(magazines[0][0], 1)
        self.assertEqual(magazines[0][1], "Tech Magazine")

if __name__ == "__main__":
    unittest.main()
