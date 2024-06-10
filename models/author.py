class Author:
    def __init__(self, id=None, name=None):
        """
        Initialize Author instance.

        Args:
            id (int): Author ID.
            name (str): Author name.
        
        Raises:
            ValueError: If name is not provided or is not a non-empty string.
        """
        self._id = id
        if name is not None:
            if not isinstance(name, str) or len(name) == 0:
                raise ValueError("Name must be a non-empty string")
            self._name = name
        else:
            raise ValueError("Name must be provided")

    @property
    def id(self):
        """Getter for author ID."""
        return self._id

    @property
    def name(self):
        """Getter for author name."""
        return self._name

    @name.setter
    def name(self, value):
        """Setter for author name (raises an error)."""
        raise AttributeError("Name cannot be changed after the author is instantiated")

    def articles(self, cursor):
        """
        Get articles written by the author.

        Args:
            cursor: Database cursor.

        Returns:
            List: Articles written by the author.
        """
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
        articles_data = cursor.fetchall()
        return articles_data

    def magazines(self, cursor):
        """
        Get magazines the author has contributed to.

        Args:
            cursor: Database cursor.

        Returns:
            List: Magazines the author has contributed to.
        """
        cursor.execute("""
            SELECT DISTINCT magazines.*
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (self._id,))
        magazines_data = cursor.fetchall()
        return magazines_data if magazines_data else None

    @classmethod
    def get_all_authors(cls, cursor):
        """
        Get all authors from the database.

        Args:
            cursor: Database cursor.

        Returns:
            List: All authors.
        """
        cursor.execute("SELECT * FROM authors")
        authors_data = cursor.fetchall()
        return [cls(id=author[0], name=author[1]) for author in authors_data]
