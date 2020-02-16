import os
import re

extension = ".txt"


class Text:
    """Text format."""
    purple = '\033[95m'
    cyan = '\033[96m'
    darkcyan = '\033[36m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    bold = '\033[1m'
    underline = '\033[4m'
    end = '\033[0m'


# TODO: Add possibility to turn on/off auto directory creation
class Directory:
    """Providing name of directory."""
    def __init__(self, dir_name):
        self.dir_name = dir_name

    def present(self):
        """Check if directory is present."""
        if not os.path.exists(self.dir_name):
            os.mkdir(self.dir_name)
            print(f"There is no directory {self.dir_name}. "
                  f"Directory {self.dir_name} was automatically created.\n")
            return True
        # TODO: A more simple and less code solution. While loop?
        else:
            return True

    # TODO: Is this function really necessary?
    def path(self):
        """Provides the path of directory."""
        path = self.dir_name + "/"
        return path

    def number_of_books(self):
        """Find out if there are books in directory."""
        if Directory.present(self):
            number = 0
            for book in os.listdir(self.dir_name):
                dir_name = "./" + self.dir_name + "/"
                if os.path.isfile(os.path.join(dir_name, book)) and re.search(extension + "$", book):
                    number += 1
            if number == 0:
                print(f"There are no books present in directory \"{self.dir_name}\".")
            return number

    # TODO: List must be sorted alphabetical
    # TODO: Try to simplify/optimize the function
    def dictionary(self):
        """Create an indexed dictionary from books in directory."""
        count = 1
        count_list = []
        book_list = []
        book_dic = []
        for book in os.listdir(self.dir_name):
            if os.path.isfile(os.path.join(self.dir_name, book)) and re.search(extension + "$", book):
                book_name = book.split(".")[0]
                count_list.append(count)
                book_list.append(book_name)
                count += 1
                book_dic = dict(zip(count_list, book_list))
        return book_dic


class MenuBooks:
    """Providing name of directory."""
    def __init__(self, dir_name):
        self.dir_name = dir_name

    def list(self):
        """List all books in directory."""
        check_dir = Directory(self.dir_name)
        check_dir.present()
        if check_dir.number_of_books():
            count = 1
            for book in os.listdir(self.dir_name):
                dir_name = "./" + self.dir_name + "/"
                if os.path.isfile(os.path.join(dir_name, book)) and re.search(extension + "$", book):
                    book_name = str(book.split(".")[0])
                    print("\t" + str(count) + ". " + book_name)
                    count += 1

    def find(self):
        """Find a book in directory."""
        check_dir = Directory(self.dir_name)
        check_dir.present()
        if check_dir.number_of_books():
            # FIXME: Input should not be empty
            find_book = input("Write the name of book: ")
            count = 1
            for book in os.listdir(self.dir_name):
                if os.path.isfile(os.path.join(self.dir_name, book)) and re.search(extension + "$", book):
                    book_name = str(book.split(".")[0])
                    my_regex = r"(.*)" + find_book + r"(.*)"
                    if re.findall(my_regex, book_name, re.IGNORECASE):
                        print(str(count) + ". " + book_name)
                        count += 1

    def select(self):
        """Select a book in directory."""
        check_dir = Directory(self.dir_name)
        check_dir.present()
        if check_dir.number_of_books():
            print("Select a book:")
            dic = check_dir.dictionary()
            for x, y in dic.items():
                print("\t" + str(x) + ". " + str(y))
            while True:
                # FIXME: Redo this section
                selected_book = input("\nSelect number of book from list. Press [ENTER] to cancel: ")
                # TODO: Selected choice must be integer
                print(type(selected_book))
                if not selected_book:
                    break
                while int(selected_book) > check_dir.number_of_books():
                    selected_book = input("Book with such number doesn't exist. Press [ENTER] to cancel: ")
                    if not selected_book:
                        break
                if not selected_book:
                    break
                else:
                    print("\nYou have selected: \"" + dic[int(selected_book)] + "\"")
                    break
            return dic[int(selected_book)]

    # TODO: 1.1 After book was created ask if user wants to add a person
    # TODO: 1.2 Ask user if wants to add another person
    # TODO: 1.3 Ask user if wants to create another book
    def create(self):
        """Create a book in directory."""
        check_dir = Directory(self.dir_name)
        check_dir.present()

        create_book = input("Please enter a name for new book: ")
        # TODO: Provide a possibility to cancel
        while not create_book:
            create_book = input("Name can't be blank. Please enter a valid name: ")

        while os.path.exists(f"./{self.dir_name}/{create_book}{extension}"):
            create_book = input("Book already exist. Please enter different name: ")
            while not create_book:
                create_book = input("Name can't be blank. Please enter a valid name: ")

        open(f"./{self.dir_name}/{create_book}{extension}", 'a').close()
        print(f"Book with name \"{create_book}\" was created.")

    def rename(self):
        """Rename a book in directory."""
        check_dir = Directory(self.dir_name)
        check_dir.present()
        if check_dir.number_of_books():
            print("Which book you want to rename:")
            dic = check_dir.dictionary()
            for x, y in dic.items():
                print("\t" + str(x) + "." + str(y))

            while True:
                old_name = input("Which book you want to rename. Press [ENTER] to cancel: ")
                if not old_name:
                    break
                if dic[int(old_name)] == "":
                    print("The book you chose has BLANK name.")
                else:
                    print("You choose: " + dic[int(old_name)])
                while old_name:
                    new_name = input("Enter new name: ")
                    while not new_name:
                        new_name = input("Name can't be blank. Please enter a valid name: ")
                    while os.path.exists(f"./{self.dir_name}/{new_name}{extension}"):
                        new_name = input("Book already exist. Please enter different name: ")
                        while not new_name:
                            new_name = input("Name can't be blank. Please enter a valid name: ")
                    os.rename(f"./{self.dir_name}/{dic[int(old_name)]}{extension}",
                              f"./{self.dir_name}/{new_name}{extension}")
                    print(f"Book \"{dic[int(old_name)]} \" was renamed to \"{new_name}\".")
                    break
                break

    def remove(self):
        """Remove a book from directory."""
        check_dir = Directory(self.dir_name)
        check_dir.present()
        # TODO: Books should be removed by option number
        remove_book = input("Which book you want to remove: ")
        while True:
            if os.path.isfile(f"./BOOKS/{remove_book}{extension}"):
                os.replace(f"./BOOKS/{remove_book}{extension}", f"./REMOVED/{remove_book}{extension}")
                print(f"Book \"{remove_book}\" was removed to directory \"REMOVED\".")
                break
            else:
                print("There is no book with such name.")
                break

    def recover(self):
        """Recover a removed book."""
        check_dir = Directory(self.dir_name)
        check_dir.present()
        recover_book = input("Which book you want to recover: ")
        while True:
            if os.path.isfile(f"./REMOVED/{recover_book}{extension}"):
                os.replace(f"./REMOVED/{recover_book}{extension}", f"./BOOKS/{recover_book}{extension}")
                print(f"Book \"{recover_book}\" was recovered to directory \"BOOKS\"")
                break
            else:
                print("There is no book with such name.")
                break


class MenuPersons:
    """Providing name of the selected book."""
    def __init__(self, book):
        self.book = book

    def view(self):
        """Print out a table with information from book.

        The width of column is dynamically adjusted.
        """
        body = open(self.book, "r")
        rows = body.readlines()
        body.close()
        rows = [x.strip() for x in rows]

        if not rows:
            print("The book is empty.")
        else:
            names_of_columns = ["ID", "First Name", "Last Name", "Email", "Phone Number", "City"]
            nr_columns = len(names_of_columns)

            every_column_length = []
            for name in names_of_columns:
                every_column_length.append(len(name))

            max_length_row_cells = []
            for nr in range(nr_columns):
                row_len = []
                for row in rows:
                    row = row.split(",")
                    row_len.append(len(row[nr]))
                max_length_row_cells.append(max(row_len))

            columns = []
            underline = []
            for nr in range(nr_columns):
                lj = max(list((every_column_length[nr], max_length_row_cells[nr])))
                columns.append(Text.bold + names_of_columns[nr].ljust(lj) + Text.end)
                underline.append(lj + 3)

            rows_ljust = []
            for row in rows:
                row = row.split(",")
                row_ljust = []
                col = 0
                if col < nr_columns:
                    for cell in row:
                        lj = []
                        for nr in range(nr_columns):
                            lj_list = [every_column_length[nr], max_length_row_cells[nr]]
                            lj.append(max(lj_list))
                        row_ljust.append(cell.ljust(lj[col]))
                        col += 1
                rows_ljust.append(row_ljust)

            pipe = Text.red + "|" + Text.end
            dash = Text.red + "-" + Text.end

            print(dash * sum(underline) + dash + Text.end)
            print(f"{pipe}", f" {pipe} ".join(columns), f"{pipe}")
            print(dash * sum(underline) + dash)
            for row in rows_ljust:
                print(f"{pipe}", f" {pipe} ".join(row) + f" {pipe}")
            print(dash * sum(underline) + dash)

    def find(self):
        """Find in book matching the keyword."""
        pass

    def create(self):
        """Create a person information in book."""
        while True:
            id_number = input("ID: ")
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            email = input("Email: ")
            phone = input("Phone Number: ")
            city = input("City: ")

            body = open(self.book, "a")
            body.write(f"{id_number},{first_name},{last_name},{email},{phone},{city}\n")
            body.close()

            another = input("Do you want to add another person?\nType \"YES\" or any key to go back: ")
            if not another == "YES":
                break

    def modify(self):
        """Modify a person information in book."""
        pass

    def export(self):
        """Export table in separate file."""
        pass

    # TODO: Possibility to recover a person
    def delete(self):
        """Delete a person from selected book."""
        pass


def clear():
    """Clear screen and display short info."""
    os.system("cls" if os.name == "nt" else "clear")
    wrote = "Marin Tailor"
    github = "git clone github.com/marintailor/python-phonebook"
    print(Text.red + Text.bold + "Phonebook in Python" + Text.end)
    print(Text.bold + "Author: " + Text.end + wrote + Text.bold + "\nGitHub: " + Text.end + github)
    print(Text.bold + Text.red + "-" * (len(github) + 8) + Text.end)


def main_menu():
    """Display main menu."""
    header = f"You are in Main menu.\n" \
             f"Please select a directory Books or Removed.\n"
    print(header)
    main_menu_options = ["Books", "Removed", "Quit"]
    count = 1
    for option in main_menu_options:
        print(f"\t{count}. {option}")
        count += 1
    return count


def books_menu():
    """Display Books directory menu."""
    header = f"You are in Books menu.\n" \
             f"Here you can list, find, create books.\n"
    print(header)
    menu_books_options = ["List", "Find", "Create", "Select", "Rename", "Remove", "Back"]
    count = 1
    for option in menu_books_options:
        print(f"\t{count}. {option}")
        count += 1


def persons_menu():
    """Display Persons of selected book menu."""
    header = f"You are in Persons menu.\n" \
             f"Here you can list, find, create persons in your selected book.\n"
    print(header)
    menu_removed_options = ["View", "Find", "Create", "Modify", "Export", "Delete", "Back"]
    count = 1
    for option in menu_removed_options:
        print(f"\t{count}. {option}")
        count += 1


def removed_menu():
    """Display Removed directory menu."""
    header = f"You are in Removed menu.\n" \
             f"Here you can list, find, recover removed books.\n"
    print(header)
    menu_removed_options = ["List", "Find", "Recover", "Back"]
    count = 1
    for option in menu_removed_options:
        print(f"\t{count}. {option}")
        count += 1


# TODO: Write menu using less code
def home():
    """Home page of Phonebook."""
    while True:
        clear()
        main_menu()
        main_menu_option = input("\nPlease select an option: ")
        # TODO: Selected option must be integer(?) between 1 and max count number
        if not main_menu_option:
            continue
        else:
            while main_menu_option == "1":
                menu_books = MenuBooks("BOOKS")
                clear()
                books_menu()
                books_menu_option = input("\nPlease select an option: ")
                while books_menu_option == "1":
                    clear()
                    menu_books.list()
                    input("\nPress [ENTER] to go back.")
                    break

                while books_menu_option == "2":
                    clear()
                    menu_books.find()
                    input("\nPress [ENTER] to go back.")
                    break

                while books_menu_option == "3":
                    clear()
                    menu_books.create()
                    input("\nPress [ENTER] to go back.")
                    break

                while books_menu_option == "4":
                    clear()
                    book = menu_books.select()
                    directory = Directory("./BOOKS")
                    path = directory.path()
                    person = MenuPersons(f"{path}{book}{extension}")

                    while True:
                        clear()
                        persons_menu()
                        print(f"\nYou are now in book \"{book}\"")
                        persons_menu_option = input("\nPlease select an option: ")
                        if not persons_menu_option:
                            continue
                        else:
                            while persons_menu_option == "1":
                                clear()
                                person.view()
                                input("\nPress [ENTER] to go back.")
                                break

                            while persons_menu_option == "2":
                                clear()
                                person.find()
                                input("\nPress [ENTER] to go back.")
                                break

                            while persons_menu_option == "3":
                                clear()
                                person.create()
                                input("\nPress [ENTER] to go back.")
                                break

                            while persons_menu_option == "4":
                                clear()
                                person.modify()
                                input("\nPress [ENTER] to go back.")
                                break

                            while persons_menu_option == "5":
                                clear()
                                person.export()
                                input("\nPress [ENTER] to go back.")
                                break

                            while persons_menu_option == "6":
                                clear()
                                person.delete()
                                input("\nPress [ENTER] to go back.")
                                break

                        if persons_menu_option == "7":
                            break

                while books_menu_option == "5":
                    clear()
                    menu_books.rename()
                    input("\nPress [ENTER] to go back.")
                    break

                while books_menu_option == "6":
                    clear()
                    menu_books.list()
                    menu_books.remove()
                    input("\nPress [ENTER] to go back.")
                    break

                if books_menu_option == "7":
                    break

            while main_menu_option == "2":
                menu_books = MenuBooks("REMOVED")
                directory = Directory("REMOVED")
                clear()
                removed_menu()
                books_menu_option = input("\nPlease select an option: ")
                while books_menu_option == "1":
                    clear()
                    menu_books.list()
                    input("\nPress [ENTER] to go back.")
                    break

                while books_menu_option == "2":
                    clear()
                    menu_books.find()
                    input("\nPress [ENTER] to go back.")
                    break

                while books_menu_option == "3":
                    clear()
                    if directory.number_of_books():
                        menu_books.list()
                        menu_books.recover()
                    input("\nPress [ENTER] to go back.")
                    break

                if books_menu_option == "4":
                    break

            if main_menu_option == "4":
                print("Have a nice day!")
                break


home()
