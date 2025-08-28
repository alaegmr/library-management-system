import xml.etree.ElementTree as ET   #parsing and manipulating XML data.

# Constants for XML file and root element -- for storing book data
XML_FILE = 'library.xml' 
ROOT_TAG = 'library'  

# Function to initialize XML file if it doesn't exist
def init_xml_file():  #creates an empty XML file with the root tag (library) if it doesn't already exist.
    root = ET.Element(ROOT_TAG)    #nfixi root 
    tree = ET.ElementTree(root)
    tree.write(XML_FILE)
#maybe i'll add smtg
# Function to add a new book to the library
def add_book(title, author, year, genre):
    tree = ET.parse(XML_FILE) #parses the XML file-- so analyse general lel fichier (ET.parse() function from the xml.etree.ElementTree which  creates a tree structure representing the XML data.)
    root = tree.getroot()   #gets the root element  <library>
           #creates a new <book> element with sub-elements for title, author, ..., and writes the updated XML back to the file.
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
     #initializes an empty list named books
    books = [] # will  store the books that match the search criteria.
                      ## loop that iterates through all <book> elements in the XML data
    for book in root.findall('book'): # findall('book') method finds all child elements with the tag name 'book' under the root element.
        # checks if the current book's attribute specified by the criteria matches the given value = if criteria is 'title', it checks if the book's title matches the value.
        if book.find(criteria).text == value:
            books.append(book) #If a book's attribute matches the search criteria, it is added to the books list using  append() method...

#After iterating through all books
    return books  #the function returns the list of books that match the search criteria.

def get_book_details(title):
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    for book in root.findall('book'):
        if book.find('title').text == title:
            author = book.find('author').text
            year = book.find('year').text
            genre = book.find('genre').text
            return author, year, genre
    return None, None, None

# Function to save modified book
def save_modified_book(old_title, new_title, new_author, new_year, new_genre):
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    found_book = False  # Flag to track if the book was found for modification

    for book in root.findall('book'):
        if book.find('title').text == old_title:
            book.find('title').text = new_title
            book.find('author').text = new_author
            book.find('year').text = new_year
            book.find('genre').text = new_genre
            found_book = True
            break  # Exit the loop after modifying the book

    if not found_book:
        raise ValueError(f"Book with title '{old_title}' not found for modification.")

    tree.write(XML_FILE)








if __name__ == "__main__":
    init_xml_file()

# Function to delete a book
def delete_book(title):
    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    for book in root.findall('book'):
        if book.find('title').text == title:
            root.remove(book)

    tree.write(XML_FILE)




if __name__ == "__main__":
    init_xml_file()  # Initialize XML file if it doesn't exist
