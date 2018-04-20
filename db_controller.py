import sqlite3

class DbController:
    """Allows user to update and search reference database"""
    def __init__(self, db_name):
        self.db_name = db_name
        #Default sql statement for displaying search results. Search terms may be concatenated to this string.
        self.search_default_sql = """SELECT Article.ArticleID, Author.LastName, Article.Year, Journal.JournalName, Article.Title 
            FROM Article 
            INNER JOIN Journal ON Article.JournalID = Journal.JournalID 
            INNER JOIN ArticleAuthor ON ArticleAuthor.ArticleID = Article.ArticleID 
            INNER JOIN Author ON ArticleAuthor.AuthorID = Author.AuthorID
            WHERE ArticleAuthor.Position = 1"""        

    def query(self, sql, data):
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA Foreign_Keys = ON")
            cursor.execute(sql, data)
            db.commit()

    def select_query(self,sql,data=None):
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            if data:
                cursor.execute(sql,data)
            else:
                cursor.execute(sql)
            results = cursor.fetchall()
        return results

    def check_journal(self, journal_name):
        #checks if journal already in table
        sql = "SELECT JournalID FROM Journal WHERE JournalName = ?"
        result = self.select_query(sql, (journal_name,))
        if result:
            return result
        return False

    def add_journal(self, journal_name):
        #adds new journal if not found in Journal table
        if not self.check_journal(journal_name):
            sql_add_journal = "INSERT INTO Journal (JournalName) VALUES (?)"
            self.query(sql_add_journal, (journal_name,))

    def check_author(self, author_name): 
        #checks if author already in Author table
        #author_name is a tuple (first name, middle initial, last name)
        if author_name[1] == "":
            sql = """SELECT AuthorID FROM Author WHERE LastName = '{2}' AND FirstName = '{0}'""".format(*author_name)
        else:
            sql = """SELECT AuthorID FROM Author WHERE LastName = '{2}' AND FirstName = '{0}' AND (MiddleInitial = '{1}' OR MiddleInitial = '')""".format(*author_name)
        result = self.select_query(sql)
        if result:
            return result
        return False

    def add_author(self, article_id, author_name, position):
        #adds author if not found in Author table
        if not self.check_author(author_name):
            sql_add_author = "INSERT INTO Author (FirstName, MiddleInitial, LastName) VALUES (?,?,?)"
            self.query(sql_add_author, author_name)
        author_id = int(self.check_author(author_name)[0][0])
        #adds middle initial if one was not provided for the author previously
        if author_name[1] != "":
            middle = self.select_query("SELECT MiddleInitial FROM Author WHERE AuthorID = ?", (author_id,))[0][0]
            if middle == "":
                self.query("UPDATE Author SET MiddleInitial = ? WHERE AuthorID = ?", (author_name[1], author_id))
        self.query("INSERT INTO ArticleAuthor (ArticleID, AuthorID, Position) VALUES (?,?,?)", (article_id, author_id, position))

    def new_article(self, title, authors, journal, year, volume, issue, first_page, last_page, file_path, keywords, notes):
        
        self.add_journal(journal)
        #gets journal_id
        journal_id = int(self.check_journal(journal)[0][0])

        #creates article entry
        sql_add_article = """INSERT INTO Article (Title, JournalID, Year, Volume, Issue,
            FirstPage, LastPage, FilePath, Keywords, Notes) VALUES (?,?,?,?,?,?,?,?,?,?)"""
        article_data = (title, journal_id, year, volume, issue, first_page, last_page, file_path, keywords, notes)
        self.query(sql_add_article, article_data)
        #gets article id
        article_id = int(self.select_query("SELECT max(ArticleID) FROM Article")[0][0])
        
        #adds authors to Author table(if necessary) and ArticleAuthor table
        position = 1
        for author in authors:
            self.add_author(article_id, author, position)
            position += 1
            
    def show_all_articles(self):
        return self.select_query(self.search_default_sql)

    def search_by_author(self, term):
        article_ids = self.select_query("""SELECT ArticleAuthor.ArticleId FROM ArticleAuthor
            INNER JOIN Author ON Author.AuthorID = ArticleAuthor.AuthorID
            WHERE Author.LastName = ?""", (term,))
        article_ids = tuple([item[0] for item in article_ids])
        if len(article_ids) == 0:
            return False
        elif len(article_ids) == 1:
            article_id = article_ids[0]
            get_results_sql = self.search_default_sql+" AND Article.ArticleID = {}".format(article_id)
        else:
            get_results_sql = self.search_default_sql+" AND Article.ArticleID in {}".format(article_ids)
        return self.select_query(get_results_sql)


    def search_by_year(self, year_from, year_to):
        if year_from == None:
            sql = self.search_default_sql+" AND Year <= {}".format(year_to)
        elif year_to == None:
            sql = self.search_default_sql+" AND Year >= {}".format(year_from)
        else:    
            sql = self.search_default_sql+" AND Year BETWEEN {0} AND {1}".format(year_from, year_to)
        return self.select_query(sql)

    def search_by_keyword(self, term):
        sql = self.search_default_sql+""" AND (Journal.JournalName LIKE '%{0}%' 
        OR Article.Keywords LIKE '%{0}%' OR Article.Title LIKE '%{0}%' 
        OR Article.Notes LIKE '%{0}%')""".format(term)
        return self.select_query(sql)

    def display_article(self, article_id):
        article_fields = self.select_query("SELECT * FROM Article WHERE ArticleID = ?", (article_id,))
        title = article_fields[0][1]
        journal_id = int(article_fields[0][2])
        year = article_fields[0][3]
        volume = article_fields[0][4]
        issue = article_fields[0][5]
        first_page = article_fields[0][6]
        last_page = article_fields[0][7]
        file_path = article_fields[0][8]
        keywords = article_fields[0][9]
        notes = article_fields[0][10]

        authors = self.get_article_authors(article_id)

        journal = self.select_query("SELECT JournalName FROM Journal WHERE JournalID = ?", (journal_id,))[0][0]

        return title, authors, journal, year, volume, issue, first_page, last_page, file_path, keywords, notes

    def edit_article(self, article_id, field, new_text):
        if field == "Journal":
            self.add_journal(new_text) #includes check to see if journal already in table
            journal_id = int(self.check_journal(new_text)[0][0])
            self.query("UPDATE Article SET JournalID = ? WHERE ArticleID = ?", (journal_id, article_id))
        else:
            self.query(f"UPDATE Article SET {field} = ? WHERE ArticleID = ?", (new_text, article_id))

    def get_article_authors(self, article_id):
        return self.select_query("""SELECT Author.AuthorID, Author.FirstName, Author.MiddleInitial, Author.LastName, ArticleAuthor.Position FROM Author
            INNER JOIN ArticleAuthor ON ArticleAuthor.AuthorID = Author.AuthorID
            WHERE ArticleAuthor.ArticleID = ? ORDER BY ArticleAuthor.Position ASC""", (article_id,))       

    def edit_author(self, author_id, new_text):
        self.query("UPDATE Author SET (FirstName, MiddleInitial, LastName) = (?, ?, ?) WHERE AuthorID = ?", (*new_text, author_id))

    def remove_author(self, article_id, author_id, position):
        self.query("DELETE FROM ArticleAuthor WHERE ArticleID = ? AND AuthorID = ?", (article_id, author_id))
        self.query("UPDATE ArticleAuthor SET Position = (Position - 1) WHERE ArticleID = ? AND Position > ?", (article_id, position))

    def change_author_position(self, article_id, author_id, new_position):
        self.query("UPDATE ArticleAuthor SET Position = ? WHERE AuthorID = ? AND ArticleID = ?", (new_position, author_id, article_id))
        
    def delete_article(self, article_id):
        self.query("DELETE FROM ArticleAuthor WHERE ArticleID = ?", (article_id,))
        self.query("DELETE FROM Article WHERE ArticleID = ?", (article_id,))

    def get_path(self, article_id):
        return self.select_query("SELECT FilePath FROM Article WHERE ArticleID = ?", (article_id,))[0][0]