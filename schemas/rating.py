from pydantic import BaseModel
from typing import List, Optional
from model.rating import Rating
from model.books import Book
from model.member import Member


class RatingSchema(BaseModel):
    """Define como uma nova avaliação deve ser representada"""
    book_id: int
    member_id: int
    stars: int


class RatingBuscaSchema(BaseModel):
    """Define a busca de avaliações por livro"""
    book_id: int = 1


class RatingViewSchema(BaseModel):
    """Define como uma avaliação será retornada"""
    id: int = 1
    book_id: int = 1
    book_title: str = "O Senhor dos Anéis"
    member_id: int = 1
    member_name: str = "Maria"
    stars: int = 5


class RatingListSchema(BaseModel):
    """Define como uma listagem de avaliações será retornada"""
    ratings: List[RatingViewSchema]


def apresenta_rating(rating: Rating, book: Book, member: Member):
    """Retorna uma representação da avaliação"""
    return {
        "id": rating.id,
        "book_id": rating.book_id,
        "book_title": book.title,
        "member_id": rating.member_id,
        "member_name": member.name,
        "stars": rating.stars,
    }


def apresenta_ratings(ratings: List[Rating]):
    """Retorna uma representação da listagem de avaliações"""
    result = []
    for r in ratings:
        if not r.book or not r.member:
            continue  # ignora avaliações órfãs
        result.append({
            "id": r.id,
            "book_id": r.book_id,
            "book_title": r.book.title,
            "member_id": r.member_id,
            "member_name": r.member.name,
            "stars": r.stars,
        })
    return {"ratings": result}