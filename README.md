# Personal-Library-Manager

## Objective

Create a **command-line Personal Library Manager** that allows users to manage their book collection. The program should let users add, remove, and search for books. Each book will be stored as a dictionary with details like title, author, publication year, genre, and read status. The program should also include a menu system, basic statistics, and optional file handling for saving and loading the library.

----------

## Requirements

### Core Features

1.  **Book Details**: Each book should have the following attributes:
    
    -   Title (string)
    -   Author (string)
    -   Publication Year (integer)
    -   Genre (string)
    -   Read Status (boolean: `True` if read, `False` if unread)
2.  **Menu System**: Implement a menu with the following options:
    
    -   Add a book
    -   Remove a book
    -   Search for a book
    -   Display all books
    -   Display statistics (total books, percentage read)
    -   Exit
3.  **Add a Book**: Prompt the user to enter the book's details and add it to the library.
    
4.  **Remove a Book**: Prompt the user to enter the title of the book to remove it from the library.
    
5.  **Search for a Book**: Allow the user to search for a book by title or author. Display all matching books.
    
6.  **Display All Books**: Show all books in the library in a formatted way.
    
7.  **Display Statistics**:
    
    -   Total number of books in the library.
    -   Percentage of books that have been read.
8.  **Exit**: Exit the program.
