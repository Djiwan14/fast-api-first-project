from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title one', 'author': 'Author one', 'category': 'science'},
    {'title': 'Title two', 'author': 'Author two', 'category': 'technology'},
    {'title': 'Title three', 'author': 'Author three', 'category': 'science'},
    {'title': 'Title four', 'author': 'Author four', 'category': 'history'},
    {'title': 'Title five', 'author': 'Author five', 'category': 'history'},
    {'title': 'Title six', 'author': 'Author six', 'category': 'mathematics'},
    {'title': 'Title six', 'author': 'Author six', 'category': 'hey'}
]

# Get Request Methods
@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def read_all_books(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# Exercise for finding book by author
@app.get("/books/get_book/")
async def get_book_by_author_name(author_name: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author_name.casefold():
            books_to_return.append(book)
    return books_to_return
########################################################
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    book_to_return = []
    for book in BOOKS:
        if (
            book.get('author').casefold() == book_author.casefold()
            and book.get('category').casefold() == category.casefold()
        ):
            book_to_return.append(book)
    return book_to_return

# Post Request Methods
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

# Put Request Methods
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book

# Delete Request Methods
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

# Fetching all books from specific author
# Exercise for finding book by author
@app.get("/books/get_book/{author_name}")
async def get_book_by_author_name(author_name: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author_name.casefold():
            books_to_return.append(book)
    return books_to_return