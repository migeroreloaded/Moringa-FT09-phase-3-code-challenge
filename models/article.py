class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        # Initialize Article attributes
        self._id = id
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id

    @property
    def id(self):
        """Getter for article ID."""
        return self._id

    @property
    def title(self):
        """Getter for article title."""
        return self._title

    @property
    def content(self):
        """Getter for article content."""
        return self._content

    @classmethod
    def create_article(cls, cursor, title, content, author_id, magazine_id):
        """Create a new article and insert it into the database."""
        cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                       (title, content, author_id, magazine_id))
        article_id = cursor.lastrowid
        return cls(article_id, title, content, author_id, magazine_id)

    @classmethod
    def get_titles(cls, cursor):
        """Get all article titles from the database."""
        cursor.execute("SELECT title FROM articles")
        titles = cursor.fetchall()
        return [title[0] for title in titles] if titles else None

    def get_author(self, cursor):
        """Get the author name of the article."""
        cursor.execute("SELECT name FROM authors WHERE id = ?", (self._author_id,))
        author_name = cursor.fetchone()
        return author_name[0] if author_name else None

    def get_magazine(self, cursor):
        """Get the magazine name of the article."""
        cursor.execute("SELECT name FROM magazines WHERE id = ?", (self._magazine_id,))
        magazine_name = cursor.fetchone()
        return magazine_name[0] if magazine_name else None
