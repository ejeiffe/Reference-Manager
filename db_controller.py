import sqlite3

class DbController:
    """Allows user to update and search reference database"""
    def __init__(self, db_name):
        self.db_name = db_name
        #Default sql statement for displaying search results. Search terms may be concatenated to this string.
        self.search_default_sql = """select Article.ArticleID, Author.LastName, Article.Year, Journal.JournalName, Article.Title 
            from Article 
            inner join Journal on Article.JournalID = Journal.JournalID 
            inner join ArticleAuthor on ArticleAuthor.ArticleID = Article.ArticleID 
            inner join Author on ArticleAuthor.AuthorID = Author.AuthorID
            where ArticleAuthor.FirstAuthor = 1"""
        self.search_headings = ["Article ID", "First Author", "Year", "Journal", "Title"]
        

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
        sql = "select JournalID from Journal where JournalName = ?"
        result = self.select_query(sql, (journal_name,))
        if result:
            return result
        return False

    def add_journal(self, journal_name):
        #adds new journal if not found in Journal table
        if not self.check_journal(journal_name):
            sql_add_journal = "insert into Journal (JournalName) values (?)"
            self.query(sql_add_journal, (journal_name,))

    def check_author(self, author_name): 
        #author_name is a tuple (first name, middle initial, last name)
        if author_name[1] == "":
            sql = """select AuthorID from Author where LastName = '{2}' AND FirstName = '{0}'""".format(*author_name)
        else:
            sql = """select AuthorID from Author where LastName = '{2}' AND FirstName = '{0}' AND MiddleInitial = '{1}'""".format(*author_name)
        result = self.select_query(sql)
        if result:
            return result
        return False

    def add_author(self, article_id, author_name, first):
        #Like add_journal, checks if author in table, adds if not
        if not self.check_author(author_name):
            sql_add_author = "insert into Author (FirstName, MiddleInitial, LastName) values (?,?,?)"
            self.query(sql_add_author, author_name)
        author_id = int(self.check_author(author_name)[0][0])
        self.query("insert into ArticleAuthor (ArticleID, AuthorID, FirstAuthor) values (?,?,?)", (article_id, author_id, first))

    def new_article(self, title, authors, journal, year, volume, issue, first_page, last_page, file_path, keywords, notes):
        
        self.add_journal(journal)
        #gets journal_id
        journal_id = int(self.check_journal(journal)[0][0])

        #creates article entry
        sql_add_article = """insert into Article (Title, JournalID, Year, Volume, Issue,
            FirstPage, LastPage, FilePath, Keywords, Notes) values (?,?,?,?,?,?,?,?,?,?)"""
        article_data = (title, journal_id, year, volume, issue, first_page, last_page, file_path, keywords, notes)
        self.query(sql_add_article, article_data)
        #gets article id
        article_id = int(self.select_query("select max(ArticleID) from Article")[0][0])
        
        #adds authors to author table(if necessary) and article author table
        for author in authors:
            if authors.index(author) == 0:
                first = 1
            else:
                first = 0
            self.add_author(article_id, author, first)
            

    def display_search_headings(self):
        for heading in self.search_headings[:3]:
            print('{0:<{width}}'.format(heading, width=15), end=' ')
        for heading in self.search_headings[3:]:
            print('{0:<{width}}'.format(heading, width=50), end=' ')
        print()

    def display_search_results(self, results):
        for entry in results:
            for item in entry[:3]:
                print('{0:<{width}}'.format(item, width=15), end=' ')
            for item in entry[3:]:
                print('{0:<{width}}'.format(item, width=50), end=' ')
            print()

    def show_results(self, results):
        if not results:
            print()
            print("No results found.")
            return False
        else:
            self.display_search_headings()
            self.display_search_results(results)
            return True

    def show_all_articles(self):
        results = self.select_query(self.search_default_sql)
        if self.show_results(results):
            return True

    def search_by_author(self, term):
        article_ids = self.select_query("""select ArticleAuthor.ArticleId from ArticleAuthor
            inner join Author on Author.AuthorID = ArticleAuthor.AuthorID
            where Author.LastName = ?""", (term,))
        article_ids = tuple([item[0] for item in article_ids])
        get_results_sql = self.search_default_sql+" and Article.ArticleID in {}".format(article_ids)
        results = self.select_query(get_results_sql)
        if self.show_results(results):
            return True
        return False

    def search_by_year(self, year_from, year_to):
        sql = self.search_default_sql+" and year between {0} and {1}".format(year_from, year_to)
        results = self.select_query(sql)
        if self.show_results(results):
            return True
        return False

    def search_by_keyword(self, term):
        sql = self.search_default_sql+""" and (Journal.JournalName like '%{0}%' 
        or Article.Keywords like '%{0}%' or Article.Title like '%{0}%' 
        or Article.Notes like '%{0}%')""".format(term)
        results = self.select_query(sql)
        if self.show_results(results):
            return True
        return False

    def display_article(self, article_id):
        article_fields = self.select_query("select * from Article where ArticleID = ?", (article_id,))
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

        authors = self.select_query("""select Author.FirstName, Author.MiddleInitial, Author.LastName from Author
            inner join ArticleAuthor on ArticleAuthor.AuthorID = Author.AuthorID
            where ArticleAuthor.ArticleID = ?""", (article_id,))

        journal = self.select_query("select JournalName from Journal where JournalID = ?", (journal_id,))[0][0]

        print("Article Details")
        print("Article ID: "+str(article_id))
        print("Title: ")
        print(title)
        print()
        print("Authors: ")
        for author in authors:
            print(*author)
        print()
        print("Journal: ")
        print(journal)
        print()
        print(f"Vol: {volume} Issue: {issue} Pages: {first_page}-{last_page}")
        print()
        print("Keywords: "+str(keywords))
        print()
        print("Notes: ")
        print(notes)
        print()
        print("File location: "+file_path)
        print()

    def edit_article(self, article_id, field, new_text):
        if field == "Journal":
            self.add_journal(new_text) #includes check to see if journal already in table
            journal_id = int(self.check_journal(journal_name)[0][0])
            self.query("update Article set JournalID = ? where ArticleID = ?", (journal_id, article_id))

        else:
            self.query(f"update Article set {field} = ? where ArticleID = ?", (new_text, article_id))

    def get_article_authors(self, article_id):
        authors = self.select_query("""select * from Author
            inner join ArticleAuthor on ArticleAuthor.AuthorID = Author.AuthorID
            where ArticleAuthor.ArticleID = ?""", (article_id,))
        print("Authors: ")
        print("ArticleID\tAuthor")
        for author in authors:
            print(str(author[0])+"\t\t"+author[1]+" "+author[2]+" "+author[3])

    def edit_author(self, author_id, field, new_text):
        self.query(f"update Author set {field} = ? where AuthorID = ?", (new_text, author_id))

    def remove_author(self, article_id, author_id):
        self.query("delete from ArticleAuthor where ArticleID = ? and AuthorID = ?", (article_id, author_id))

    def change_first_author(self, new_first_id, article_id):
        old_first_id = self.select_query("select AuthorID from ArticleAuthor where ArticleID = ? and FirstAuthor = 1", (article_id,))[0][0]
        self.query("update ArticleAuthor set FirstAuthor = 0 where AuthorID = ? and ArticleID = ?", (old_first_id, article_id))
        self.query("update ArticleAuthor set FirstAuthor = 1 where AuthorID = ? and ArticleID = ?", (new_first_id, article_id))

    def delete_article(self, article_id):
        self.query("delete from ArticleAuthor where ArticleID = ?", (article_id,))
        self.query("delete from Article where ArticleID = ?", (article_id,))

    def get_path(self, article_id):
        return self.select_query("select FilePath from Article where ArticleID = ?", (article_id,))[0][0]