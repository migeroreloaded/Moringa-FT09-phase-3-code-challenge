from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Create an author
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (author_name,))
        author_id = cursor.lastrowid
        author = Author(id=author_id, name=author_name)

        # Create a magazine
        magazine = Magazine(name=magazine_name, category=magazine_category)
        magazine.create_magazine(cursor)

        # Create an article
        article = Article.create_article(cursor, article_title, article_content, author.id, magazine.id)

        conn.commit()

        # Display the created objects
        print("\nCreated Author:")
        print(f"ID: {author.id}, Name: {author.name}")

        print("\nCreated Magazine:")
        print(f"ID: {magazine.id}, Name: {magazine.name}, Category: {magazine.category}")

        print("\nCreated Article:")
        print(f"ID: {article.id}, Title: {article.title}, Content: {article.content}")

        # Additional functionality to showcase object methods

        # Fetch all articles by the author
        author_articles = author.articles(cursor)
        if author_articles:
            print("\nArticles by Author:")
            for art in author_articles:
                print(dict(art))  # Convert to dictionary for readability
        else:
            print("\nNo articles by this author.")

        # Fetch all magazines the author has contributed to
        author_magazines = author.magazines(cursor)
        if author_magazines:
            print("\nMagazines by Author:")
            for mag in author_magazines:
                print(dict(mag))  # Convert to dictionary for readability
        else:
            print("\nNo magazines by this author.")

        # Fetch all articles in the magazine
        magazine_articles = magazine.articles(cursor)
        if magazine_articles:
            print("\nArticles in Magazine:")
            for art in magazine_articles:
                print(dict(art))  # Convert to dictionary for readability
        else:
            print("\nNo articles in this magazine.")

        # Fetch all contributors to the magazine
        magazine_contributors = magazine.contributors(cursor)
        if magazine_contributors:
            print("\nContributors to Magazine:")
            for cont in magazine_contributors:
                print(dict(cont))  # Convert to dictionary for readability
        else:
            print("\nNo contributors to this magazine.")

        # Fetch article titles for the magazine
        magazine_article_titles = magazine.article_titles(cursor)
        if magazine_article_titles:
            print("\nArticle Titles in Magazine:")
            for title in magazine_article_titles:
                print(title)
        else:
            print("\nNo article titles in this magazine.")

        # Fetch contributing authors with more than two articles
        contributing_authors = magazine.contributing_authors(cursor)
        if contributing_authors:
            print("\nContributing Authors with more than two articles in Magazine:")
            for author in contributing_authors:
                print(dict(author))  # Convert to dictionary for readability
        else:
            print("\nNo contributing authors with more than two articles in this magazine.")

    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
