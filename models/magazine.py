class Magazine:
    def __init__(self, id=None, name=None, category=None):
        """
        Initialize Magazine instance.

        Args:
            id (int): Magazine ID.
            name (str): Magazine name.
            category (str): Magazine category.
        """
        self._id = id
        self._name = name
        self._category = category

    @property
    def id(self):
        """Getter for magazine ID."""
        return self._id

    @property
    def name(self):
        """Getter for magazine name."""
        return self._name

    @name.setter
    def name(self, value):
        """
        Setter for magazine name.

        Args:
            value (str): New magazine name.

        Raises:
            ValueError: If the name is not a string between 2 and 16 characters.
        """
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Name must be a string between 2 and 16 characters")

    @property
    def category(self):
        """Getter for magazine category."""
        return self._category

    @category.setter
    def category(self, value):
        """
        Setter for magazine category.

        Args:
            value (str): New category name.

        Raises:
            ValueError: If the category is not a non-empty string.
        """
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string")

    def create_magazine(self, cursor):
        """
        Create a new magazine and insert it into the database.

        Args:
            cursor: Database cursor.
        """
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self._name, self._category))
        self._id = cursor.lastrowid

    @classmethod
    def get_all_magazines(cls, cursor):
        """
        Get all magazines from the database.

        Args:
            cursor: Database cursor.

        Returns:
            List: All magazines.
        """
        cursor.execute("SELECT * FROM magazines")
        all_magazines = cursor.fetchall()
        return [cls(magazine_data[0], magazine_data[1], magazine_data[2]) for magazine_data in all_magazines]

    def articles(self, cursor):
        """
        Get articles belonging to this magazine.

        Args:
            cursor: Database cursor.

        Returns:
            List: Articles belonging to this magazine.
        """
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self._id,))
        articles_data = cursor.fetchall()
        return articles_data

    def contributors(self, cursor):
        """
        Get contributors of this magazine.

        Args:
            cursor: Database cursor.

        Returns:
            List: Contributors of this magazine.
        """
        cursor.execute("""
            SELECT authors.*
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self._id,))
        contributors_data = cursor.fetchall()
        return contributors_data

    def article_titles(self, cursor):
        """
        Get titles of articles belonging to this magazine.

        Args:
            cursor: Database cursor.

        Returns:
            List: Titles of articles belonging to this magazine.
        """
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self._id,))
        titles = [row[0] for row in cursor.fetchall()]
        return titles if titles else None

    def contributing_authors(self, cursor):
        """
        Get authors contributing more than 2 articles to this magazine.

        Args:
            cursor: Database cursor.

        Returns:
            List: Authors contributing more than 2 articles to this magazine.
        """
        cursor.execute("""
            SELECT authors.*, COUNT(*) AS article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self._id,))
        authors_data = cursor.fetchall()
        return authors_data if authors_data else None
