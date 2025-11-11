from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int, published_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_field=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(lt=2025)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2016
            }
        }
    }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5, 2016),
    Book(2, "Be fast with FastAPI", "codingwithroby", "A great book!", 5, 2016),
    Book(3, "Master Endpoints", "codingwithroby", "An awesome book!", 5, 2014),
    Book(4, "HP1", "Author 1", "Book description", 2, 1985),
    Book(5, "HP2", "Author 2", "Book description", 3, 1246),
    Book(6, "HP3", "Author 3", "Book description", 1, 2016),
]


@app.get("/books", tags=["Fetching Data"])
async def read_all_books():
    return BOOKS


@app.get("/books/{published_year}", tags=["Fetching Data"])
async def get_book_by_year(published_year: int = Path(lt=2026)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_year:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_id}/", tags=["Fetching Data"])
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books/", tags=["Fetching Data"])
async def get_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book", tags=["Creating Data"])
async def create_book(book_request: BookRequest):
    # Book(**book_request.dict()) converting the request to Book object
    # Book(**book_request.dict()) = Book(**book_request.model_dump())
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


# This method helps us to auto increment the id of the books that are being added
def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book


@app.put("/books/update_book", tags=["Updating Data"])
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.delete("/books/{book_id}", tags=["Deleting Data"])
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
