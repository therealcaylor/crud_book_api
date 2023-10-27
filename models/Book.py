from pydantic import BaseModel, Field
from typing import Optional


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.author = author
        self.description = description
        self.id = id
        self.rating = rating
        self.title = title


class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=1000)
    rating: int = Field(gt=-1, lt=6)

    class Config:
        json_schema_extra={
            'example':{
                'title':'new book',
                'author':'coding stuff',
                'description': 'new description',
                'rating':5
            }
        }