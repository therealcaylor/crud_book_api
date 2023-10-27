from fastapi import FastAPI, Body, Path, Query, HTTPException
from models.Book import Book, BookRequest
from starlette import status
# ----------------------------------------

app = FastAPI()

BOOKS = [
    Book(id=1, title="book1", author="john",
         description="book written by john", rating=1),
    Book(id=2, title="book2", author="jim",
         description="book written by jim", rating=4),
    Book(id=3, title="book3", author="jum",
         description="book written by jum", rating=5),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{id}", status_code=status.HTTP_200_OK)
async def read_book(id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail='book not found!')


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(rating: int = Query(gt=-1, lt=6)):
    returning_books = []
    for book in BOOKS:
        if book.rating == rating:
            returning_books.append(book)
    return returning_books


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


@app.put("/books", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    found = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            found = True
    if not found:
        raise HTTPException(status_code=404, detail="book not found!")


@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delet_book(id: int = Path(gt=0)):
    found = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            BOOKS.pop(i)
            found = True
            break
    if not found:
        raise HTTPException(status_code=404, detail="book not found!")


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id+1
    else:
        book.id = 1
    return book
