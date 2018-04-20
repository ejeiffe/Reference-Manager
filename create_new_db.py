import sqlite3

def create_new_db(db_name):
    """Sets up tables for new database"""
    
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()

        #create author_article table
        cursor.execute("""CREATE TABLE ArticleAuthor(
            ArticleAuthorID integer,
            ArticleID integer,
            AuthorID integer,
            Position integer,
            PRIMARY KEY(ArticleAuthorID),
            FOREIGN KEY(ArticleID) REFERENCES Article(ArticleID),
            FOREIGN KEY(AuthorID) REFERENCES Author(AuthorID));""")

        #create article table
        cursor.execute("""CREATE TABLE Article(
            ArticleID integer,
            Title text,
            JournalID integer,
            Year integer,
            Volume text,
            Issue text,
            FirstPage text,
            LastPage text,
            FilePath text,
            Keywords text,
            Notes text,
            PRIMARY KEY(ArticleID),
            FOREIGN KEY(JournalID) REFERENCES Journal(JournalID));""")


        #create author table
        cursor.execute("""CREATE TABLE Author(
            AuthorID integer,
            FirstName text,
            MiddleInitial text,
            LastName text,
            PRIMARY KEY(AuthorID));""")


        #create journal table
        cursor.execute("""CREATE TABLE Journal(
            JournalID integer,
            JournalName text,
            PRIMARY KEY(JournalID));""")

        db.commit()



        