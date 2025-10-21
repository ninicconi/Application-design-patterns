class Book:
    def __init__(self, title, author, isbn, copies):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.copies = copies


class Reader:
    def __init__(self, name, reader_id):
        self.name = name
        self.reader_id = reader_id
        self.borrowed_books = []


class Library:
    def __init__(self):
        self.books = []
        self.readers = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                self.books.remove(b)
                break

    def register_reader(self, reader):
        self.readers.append(reader)

    def issue_book(self, reader_id, isbn):
        reader = next((r for r in self.readers if r.reader_id == reader_id), None)
        book = next((b for b in self.books if b.isbn == isbn and b.copies > 0), None)
        if reader and book:
            reader.borrowed_books.append(book)
            book.copies -= 1
            print(f"{book.title} issued to {reader.name}")
        else:
            print("Book not available or reader not found")

    def return_book(self, reader_id, isbn):
        reader = next((r for r in self.readers if r.reader_id == reader_id), None)
        if not reader:
            print("Reader not found")
            return
        for book in reader.borrowed_books:
            if book.isbn == isbn:
                book.copies += 1
                reader.borrowed_books.remove(book)
                print(f"{book.title} returned by {reader.name}")
                return
        print("Book not found in borrowed list")


library = Library()
b1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "1111", 3)
b2 = Book("1984", "George Orwell", "2222", 2)
library.add_book(b1)
library.add_book(b2)

r1 = Reader("Alice", "R1")
r2 = Reader("Bob", "R2")
library.register_reader(r1)
library.register_reader(r2)

library.issue_book("R1", "1111")
library.issue_book("R2", "2222")
library.return_book("R1", "1111")
