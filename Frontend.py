import tkinter as tk
from tkinter import messagebox
import xml.etree.ElementTree as ET
from Backend import delete_book, save_modified_book, get_book_details  # Import all necessary functions

# Constants for XML file and root element -- for storing book data
XML_FILE = 'library.xml'
ROOT_TAG = 'library'

# Function to initialize XML file if it doesn't exist
def init_xml_file():
    root = ET.Element(ROOT_TAG)
    tree = ET.ElementTree(root)
    tree.write(XML_FILE)

# Function to add a new book to the library
def add_book(title, author, year, genre):
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    book = ET.SubElement(root, 'book')
    ET.SubElement(book, 'title').text = title
    ET.SubElement(book, 'author').text = author
    ET.SubElement(book, 'year').text = year
    ET.SubElement(book, 'genre').text = genre
    tree.write(XML_FILE)

# Function to search for books based on criteria
def search_books(criteria, value):
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    books = []
    for book in root.findall('book'):
        if book.find(criteria).text == value:
            books.append(book)
    return books

# Function to retrieve all books from XML file
def retrieve_all_books():
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    books = root.findall('book')
    return books

# Function to display all books in the "All Books" section
def display_all_books():
    books = retrieve_all_books()
    books_text.delete(1.0, tk.END)
    global book_checkboxes
    book_checkboxes = []  # Clear the list before updating
    for book in books:
        book_title = book.find('title').text
        book_author = book.find('author').text
        book_year = book.find('year').text
        book_genre = book.find('genre').text
        books_text.insert(tk.END, f"Title: {book_title} | Author: {book_author} | Year: {book_year} | Genre: {book_genre}\n")

        # Add a checkbox for each book
        checkbox_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(books_text, text="Select", variable=checkbox_var, onvalue=True, offvalue=False)
        book_checkboxes.append((book, checkbox_var))  # Store a reference to the checkbox and book
        books_text.window_create(tk.END, window=checkbox)
        books_text.insert(tk.END, "\n")  # Newline after each book

# Function to refresh books display
def refresh_books_display():
    display_all_books()

# Function to delete selected books
def delete_selected_books():
    selected_books = [book for book, var in book_checkboxes if var.get()]
    if not selected_books:
        messagebox.showwarning("Delete Books", "Please select books to delete.")
        return

    for book in selected_books:
        delete_book(book.find('title').text)

    refresh_books_display()  # Refresh display after deletion

# Create the main window
window = tk.Tk()
window.title("Library Management System")
window.geometry("800x600")  # Set window size

# Global variable to store books list
books_list = []

# Function to switch frames (navigation)
def show_frame(frame):
    frame.tkraise()

# Function to refresh books display
def refresh_books_display():
    global books_list
    books_list = search_books("title", "")
    display_all_books()
    # Refresh the GUI elements after updating the books display
    window.update_idletasks()

# Function to modify a book
def modify_book_command(title):
    modify_window = tk.Toplevel(window)
    modify_window.title("Modify Book")

    tk.Label(modify_window, text="New Author:").pack()
    new_author_entry = tk.Entry(modify_window)
    new_author_entry.pack()

    tk.Label(modify_window, text="New Year:").pack()
    new_year_entry = tk.Entry(modify_window)
    new_year_entry.pack()

    tk.Label(modify_window, text="New Genre:").pack()
    new_genre_entry = tk.Entry(modify_window)
    new_genre_entry.pack()

    modify_book_button = tk.Button(modify_window, text="Modify Book",
                                   command=lambda: modify_book(title, new_author_entry.get(), new_year_entry.get(),
                                                               new_genre_entry.get()))
    modify_book_button.pack()

# Function to add a book to the library
def add_book_command():
    title = title_entry.get()
    author = author_entry.get()
    year = year_entry.get()
    genre = genre_entry.get()
    add_book(title, author, year, genre)
    clear_entries()
    refresh_books_display()
    status_label.config(text="Book added successfully!")

# Function to search for books based on criteria
def search_books_command():
    criteria = criteria_var.get()
    value = value_entry.get()
    books = search_books(criteria, value)
    result_text.delete(1.0, tk.END)
    if books:
        for book in books:
            result_text.insert(tk.END, f"Title: {book.find('title').text}\n")
            result_text.insert(tk.END, f"Author: {book.find('author').text}\n")
            result_text.insert(tk.END, f"Year: {book.find('year').text}\n")
            result_text.insert(tk.END, f"Genre: {book.find('genre').text}\n\n")
    else:
        result_text.insert(tk.END, "No books found.")

# Function to modify selected book
# Function to modify selected book
def modify_selected_book():
    selected_books = [book for book, var in book_checkboxes if var.get()]
    if not selected_books:
        messagebox.showwarning("Modify Book", "Please select a book to modify.")
        return

    title = selected_books[0].find('title').text  # Assume only one book can be modified at a time
    author, year, genre = get_book_details(title)

    # Populate input fields with book details
    title_entry.delete(0, tk.END)
    title_entry.insert(0, title)

    author_entry.delete(0, tk.END)
    author_entry.insert(0, author)

    year_entry.delete(0, tk.END)
    year_entry.insert(0, year)

    genre_entry.delete(0, tk.END)
    genre_entry.insert(0, genre)

    status_label.config(text="Modifying book: " + title)

    # Update save button command to use modified book details
    save_changes_button.config(command=lambda: save_modified_book_command(title, title_entry.get(), author_entry.get(), year_entry.get(), genre_entry.get()))

# Add a "Modify Selected Book" button
modify_button = tk.Button(window, text="Modify Selected Book", command=modify_selected_book, bg="orange", fg="white")
modify_button.pack()

# Function to save modified book


# Update save modified book command to accept modified book details
def save_modified_book_command(old_title, new_title, new_author, new_year, new_genre):
    try:
        save_modified_book(old_title, new_title, new_author, new_year, new_genre)
        status_label.config(text="Book modifications saved.")
        refresh_books_display()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Add a "Save Changes" button
save_changes_button = tk.Button(window, text="Save Changes", command=save_modified_book_command, bg="yellow", fg="black")
save_changes_button.pack()

# Function to clear entry fields
def clear_entries():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)

# Create input fields and labels
tk.Label(window, text="Title:").pack()
title_entry = tk.Entry(window)
title_entry.pack()

tk.Label(window, text="Author:").pack()
author_entry = tk.Entry(window)
author_entry.pack()

tk.Label(window, text="Year:").pack()
year_entry = tk.Entry(window)
year_entry.pack()

tk.Label(window, text="Genre:").pack()
genre_entry = tk.Entry(window)
genre_entry.pack()

# Add Book button
add_button = tk.Button(window, text="Add Book", command=add_book_command, bg="green", fg="white")
add_button.pack()

# Search Books section
tk.Label(window, text="Search Criteria:").pack()
criteria_var = tk.StringVar(window)
criteria_var.set("title")
criteria_option = tk.OptionMenu(window, criteria_var, "title", "author", "year", "genre")
criteria_option.pack()

value_entry = tk.Entry(window)
value_entry.pack()

search_button = tk.Button(window, text="Search Books", command=search_books_command, bg="blue", fg="white")
search_button.pack()

# Result text area
tk.Label(window, text="Search Results:", bg="black", fg="white").pack()
result_text = tk.Text(window, height=10, width=50)
result_text.pack()

# Display Books section using a text widget
tk.Label(window, text="All Books:", bg="black", fg="white").pack()
books_text = tk.Text(window, height=10, width=100)
books_text.pack()

# Create a list to store selected books and checkboxes
book_checkboxes = []

# Display all books and checkboxes
display_all_books()

# Delete Book button
delete_button = tk.Button(window, text="Delete Selected Books", command=delete_selected_books, bg="red", fg="white")
delete_button.pack()

# Status label
status_label = tk.Label(window, text="", fg="green")
status_label.pack()

# Initialize books display
refresh_books_display()

# Run the main loop
window.mainloop()

