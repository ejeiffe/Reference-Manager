import os.path
import sqlite3

from create_new_db import *
from db_controller import *

def main_menu():
    print()
    print("Main Menu: ")
    print()
    print("1. New article")
    print("2. Search")
    print("0. Exit")
    print()

def search_menu():
    print()
    print("Search Menu: ")
    print()
    print("1. Show all articles")
    print("2. Search by Author")
    print("3. Search by Keyword")
    print("4. Search by Year")
    print("0. Return to main menu")
    print()

def search_results_menu():
    print()
    print("Search Results Menu: ")
    print()
    print("1. Select article")
    print("2. Search again")
    print("0. Return to main menu")
    print()

def article_menu():
    print()
    print("Article Options: ")
    print()
    print("1. Edit article")
    print("2. Open pdf")
    print("3. Delete article")
    print("4. Return to search results")
    print("5. Return to search menu")
    print("0. Return to main menu")
    print()

def edit_menu():
    print()
    print("Edit Menu: ")
    print()
    print("1. Edit Authors")
    print("2. Edit Title")
    print("3. Edit Journal")
    print("4. Edit Year")
    print("5. Edit Volume")
    print("6. Edit Issue")
    print("7. Edit First Page")
    print("8. Edit Last Page")
    print("9. Edit File Location")
    print("10. Edit Keywords")
    print("11. Edit Notes")
    print("0. Return to article options")
    print()

def author_edit_menu():
    print()
    print("Edit Authors Menu: ")
    print()
    print("1. Add author")
    print("2. Remove author")
    print("3. Edit author name")
    print("4. Change first author")
    print("0. Return to edit menu")
    print()

def menu_select(len_menu):
    valid = False
    while not valid:
        try:
            selection = int(input("Select an option: "))
            if selection in range(len_menu):
                valid = True
            else:
                print(f"Enter a number between 0 and {str(len_menu-1)}")
        except:
            print(f"Enter a number between 0 and {str(len_menu-1)}")
    return selection

def new_article_inputs():
    title = input("Title: ")

    authors = []
    first_author_first = input("First Author:\nFirst name: ").capitalize()
    first_author_middle = input("Middle initial: ").upper()
    first_author_last = input("Last name: ").capitalize()
    authors.append((first_author_first, first_author_middle, first_author_last))
        
    add_author = True

    while add_author:
        add = input("Add another author? y/n: ")
        if add.lower() == 'y':
            author_first = input("First name: ").capitalize()
            author_middle = input("Middle initial: ").upper()
            author_last = input("Last name: ").capitalize()
            authors.append((author_first, author_middle, author_last))
        else:
            add_author = False

    journal = input("Journal: ")
    year = int(input("Year: "))
    volume = input("Volume: ")
    issue = input("Issue: ")
    first_page = input("First page: ")
    last_page = input("Last page: ")
    file_path = input("PDF file location: ")
    keywords = input("Keywords: ")
    notes = input("Notes: ")

    return title, authors, journal, year, volume, issue, first_page, last_page, file_path, keywords, notes

def author_inputs():
    author_first = input("First name: ")
    author_middle = input("Middle initial: ")
    author_last = input("Last name: ")

    return author_first, author_middle, author_last

if __name__ == "__main__":
    #creates new database if not found in folder
    if not os.path.exists("references.db"):
        create_new_db("references.db")
        print("New database created")
    controller = DbController("references.db")
    db_open = True
    while db_open:
        main_menu()
        main_select = menu_select(3)
        if main_select == 1:
            #Creates new article entry based on user inputs
            inputs = new_article_inputs()
            controller.new_article(*inputs)
        elif main_select == 2:
            #Go to search menu
            searching = True
            results = False
            while searching:
                search_menu()
                search_select = menu_select(5)
                if search_select == 1:
                    if controller.show_all_articles():
                        results = True
                elif search_select == 2:
                    name = input("Enter author surname: ").capitalize()
                    if controller.search_by_author(name):
                        results = True
                elif search_select == 3:
                    term = input("Enter keyword: ")
                    if controller.search_by_keyword(term):
                        results = True
                elif search_select == 4:
                    year_from = int(input("Search from year: "))
                    year_to = int(input("Search to year: "))
                    if controller.search_by_year(year_from, year_to):
                        results = True
                elif search_select == 0:
                    searching = False
                #If results found, go to search results menu
                while results:
                    search_results_menu()
                    results_select = menu_select(3)
                
                    if results_select == 1:
                        article_id = int(input("Enter Article ID to display: "))
                        controller.display_article(article_id)
                        article_options = True
                        #Go to article options menu
                        while article_options:
                            article_menu()
                            article_select = menu_select(6)
                            if article_select == 1:
                                edit = True
                                #Go to edit menu
                                while edit:
                                    edit_menu()
                                    edit_select = menu_select(12)
                                    if edit_select == 0:
                                        edit = False
                                    elif edit_select == 1:
                                        #Go to edit authors menu
                                        controller.get_article_authors(article_id)
                                        author_edit_menu()
                                        author_select = menu_select(5)
                                        if author_select == 1:
                                            #Add new author
                                            author_name = author_inputs()
                                            controller.add_author(article_id, author_name, 0)
                                        elif author_select == 2:
                                            #Remove author
                                            author_id = int(input("Enter ID of author to remove: "))
                                            controller.remove_author(article_id, author_id)
                                        elif author_select == 3:
                                            #Edit author details
                                            author_id = int(input("Enter ID of author to edit: "))
                                            new_first = input("Enter new first name or press enter to continue: ")
                                            if new_first != "":
                                                controller.edit_author(author_id, "FirstName", new_first)
                                            new_middle = input("Enter new middle initial or press enter to continue: ")
                                            if new_middle != "":
                                                controller.edit_author(author_id, "MiddleInitial", new_middle)
                                            new_last = input("Enter new last name or press enter to continue: ")
                                            if new_last != "":
                                                controller.edit_author(author_id, "LastName", new_first)
                                        elif author_select == 4:
                                            #Change first author
                                            new_first_id = input("Enter ID of new first author: ")
                                            controller.change_first_author(new_first_id, article_id)
                                        elif author_select == 0:
                                            continue
                                            #Return to edit menu
                                    else:
                                        fields = ("Title", "Journal", "Year", "Volume", "Issue", "FirstPage", "LastPage", "FilePath", "Keywords", "Notes")
                                        field = fields[edit_select-2]
                                        new_text = input(f"Enter new {field}: ")
                                        if field == "Year":
                                            new_text = int(new_text)
                                        controller.edit_article(article_id, field, new_text)                               
                            elif article_select == 2:
                                #Get pdf file path from db and open file with default program
                                path = controller.get_path(article_id)
                                if path == "":
                                    print("No file location entered")
                                else:
                                    try:
                                        os.startfile(path)
                                    except:
                                        print("File not found. Check file path.")
                            elif article_select == 3:
                                #Delete article
                                del_choice = input("Are you sure? y/n: ")
                                if del_choice.lower() == "y":
                                    controller.delete_article(article_id)
                                    print("Article deleted.")
                                    article_options = False
                                    results = False
                                    searching = False
                                else:
                                    print("Article not deleted. Returning to article options.")
                            elif article_select in (4,5,0):
                                article_options = False
                                #Return to search results menu
                                if article_select in (5,0):
                                    results = False
                                    #Return to search menu
                                    if article_select == 0:
                                        searching = False
                                        #Return to main menu
                    elif results_select in (2,0):
                        results = False
                        #Return to search menu
                        if results_select == 0:
                            searching = False
                            #Return to main menu

        elif main_select == 0:
            db_open = False
            #Exit
