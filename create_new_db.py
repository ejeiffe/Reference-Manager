import sqlite3

def create_new_db(db_name):
    """Sets up tables for new database"""
    
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()

        #create author_article table
        cursor.execute("""create table ArticleAuthor(
            ArticleAuthorID integer,
            ArticleID integer,
            AuthorID integer,
            FirstAuthor integer,
            primary key(ArticleAuthorID),
            foreign key(ArticleID) references Article(ArticleID),
            foreign key(AuthorID) references Author(AuthorID));""")

        #create article table
        cursor.execute("""create table Article(
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
            primary key(ArticleID),
            foreign key(JournalID) references Journal(JournalID));""")


        #create author table
        cursor.execute("""create table Author(
            AuthorID integer,
            FirstName text,
            MiddleInitial text,
            LastName text,
            primary key(AuthorID));""")


        #create journal table
        cursor.execute("""create table Journal(
            JournalID integer,
            JournalName text,
            primary key(JournalID));""")

        db.commit()



        