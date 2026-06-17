from pydantic import BaseModel
from typing import Optional, List
from model.books import Book
from datetime import datetime

class BookDeleteSchema(BaseModel):
    """Define como deve ser a estrutura para deletar um livro, feita pelo título"""
    title: str = "O Senhor dos Anéis"

class BookSchema(BaseModel):
    """Define como um novo livro a ser inserido deve ser representado"""
    title: str = "O Senhor dos Anéis"
    author: str = "J.R.R. Tolkien"
    genre: str = "Fantasia"
    read_date: str = "03/2024"
    recommended_by: str = "Maria"


class BookFilterSchema(BaseModel):
    """Define os filtros disponíveis para busca de livros"""
    title: Optional[str] = None
    author: Optional[str] = None
    recommended_by: Optional[str] = None
    genre: Optional[str] = None
    read_date: Optional[str] = None


class BookViewSchema(BaseModel):
    """Define como um livro será retornado"""
    id: int = 1
    title: str = "O Senhor dos Anéis"
    author: str = "J.R.R. Tolkien"
    genre: str = "Fantasia"
    read_date: str = "03/2024"
    recommended_by: str = "Maria"
    avg_stars: Optional[float] = None
    total_ratings: int = 0


class BookListSchema(BaseModel):
    """Define como uma listagem de livros será retornada"""
    books: List[BookViewSchema]


class BookDelSchema(BaseModel):
    """Define o retorno após remoção de um livro"""
    message: str
    title: str


class MessageSchema(BaseModel):
    """Define uma mensagem simples de retorno"""
    message: str


def apresenta_book(book: Book):
    """Retorna uma representação do livro com média de estrelas"""
    try:
        ratings = book.ratings or []
    except Exception:
        ratings = []
    
    avg = round(sum(r.stars for r in ratings) / len(ratings), 1) if ratings else None

    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "genre": book.genre,
        "read_date": book.read_date.strftime("%m/%Y"),
        "recommended_by": book.recommended_by,
        "avg_stars": avg,
        "total_ratings": len(ratings),
    }


def apresenta_books(books: List[Book]):
    """Retorna uma representação da listagem de livros com médias"""
    return {"books": [apresenta_book(b) for b in books]}