from flask_openapi3 import APIBlueprint, Tag
from urllib.parse import unquote
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from model import Session
from model.books import Book
from logger import logger

from schemas import (
    BookSchema,
    BookDeleteSchema,
    BookViewSchema,
    BookListSchema,
    BookFilterSchema,
    BookDelSchema,
    MessageSchema,
    ErrorSchema,
    apresenta_book,
    apresenta_books,
)

books_tag = Tag(name="Books", description="Adição, visualização, busca e remoção de livros do clube")

books_bp = APIBlueprint(
    "books",
    __name__,
    url_prefix="/books",
    abp_tags=[books_tag]
)


@books_bp.get("/", responses={"200": BookListSchema})
def get_books():
    """Faz a busca por todos os livros cadastrados

    Retorna uma representação da listagem de livros.
    """
    logger.debug("Coletando livros")
    session = Session()
    books = session.query(Book).order_by(Book.read_date.desc()).all()

    if not books:
        session.close()
        return {"books": []}, 200

    logger.debug(f"{len(books)} livros encontrados")
    result = apresenta_books(books)
    session.close()
    return result, 200


@books_bp.post("/", responses={"200": BookViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_book(body: BookSchema):
    """Adiciona um novo Livro à base de dados

    Retorna uma representação do livro cadastrado.
    """
    logger.debug(f"Adicionando livro: '{body.title}'")
    try:
        session = Session()

        month, year = body.read_date.split("/")
        read_date = datetime(int(year), int(month), 1)

        book = Book(
            title=body.title,
            author=body.author,
            genre=body.genre,
            read_date=read_date,
            recommended_by=body.recommended_by
        )

        session.add(book)
        session.commit()
        logger.debug(f"Livro adicionado: '{book.title}'")
        result = apresenta_book(book)
        session.close()
        return result, 200

    except IntegrityError:
        error_msg = "Livro com mesmo título já salvo na base :/"
        logger.warning(f"Erro ao adicionar livro '{body.title}': {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar o livro :/"
        logger.warning(f"Erro ao adicionar livro '{body.title}': {error_msg}")
        return {"message": error_msg}, 400


@books_bp.delete("/book", responses={"200": BookDelSchema, "404": ErrorSchema})
def delete_book(query: BookDeleteSchema):
    """Deleta um livro a partir do título informado

    Retorna uma mensagem de confirmação da remoção.
    """
    title = unquote(unquote(query.title))
    logger.debug(f"Deletando livro: '{title}'")
    session = Session()

    book = session.query(Book).filter(Book.title == title).first()

    if not book:
        session.close()
        error_msg = "Livro não encontrado na base :/"
        logger.warning(f"Erro ao deletar livro '{title}': {error_msg}")
        return {"message": error_msg}, 404

    session.delete(book)
    session.commit()
    session.close()

    logger.debug(f"Livro deletado: '{title}'")
    return {"message": "Livro removido", "title": title}, 200


@books_bp.get("/filter", responses={"200": BookListSchema})
def filter_books(query: BookFilterSchema):
    """Filtra livros por título, autor, gênero, quem indicou e/ou data de leitura

    Retorna uma lista de livros filtrada.
    """
    logger.debug(f"Filtrando livros - título: {query.title}, autor: {query.author}, gênero: {query.genre}, indicado por: {query.recommended_by}, data: {query.read_date}")
    session = Session()
    q = session.query(Book)

    if query.title:
        q = q.filter(Book.title.ilike(f"%{query.title}%"))
    if query.author:
        q = q.filter(Book.author == query.author)
    if query.genre:
        q = q.filter(Book.genre == query.genre)
    if query.recommended_by:
        q = q.filter(Book.recommended_by == query.recommended_by)
    if query.read_date:
        try:
            month, year = query.read_date.split("/")
            date_filter = datetime(int(year), int(month), 1)
            q = q.filter(Book.read_date == date_filter)
        except ValueError:
            pass

    books = q.order_by(Book.read_date.desc()).all()
    result = apresenta_books(books)
    session.close()
    return result, 200


@books_bp.get("/stats")
def stats():
    """Retorna estatísticas: autor mais lido, top 3 gêneros e total de livros
    """
    logger.debug("Coletando estatísticas")
    session = Session()
    books = session.query(Book).all()
    session.close()

    total = len(books)

    if not books:
        return {
            "total_books": 0,
            "most_read_author": None,
            "most_read_genre": None,
            "top_genres": []
        }, 200

    author_count = {}
    genre_count = {}

    for b in books:
        author_count[b.author] = author_count.get(b.author, 0) + 1
        genre_count[b.genre]   = genre_count.get(b.genre, 0)  + 1

    top_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)[:3]

    return {
        "total_books":      total,
        "most_read_author": max(author_count, key=author_count.get),
        "most_read_genre":  max(genre_count,  key=genre_count.get),
        "top_genres": [{"genre": g, "count": c} for g, c in top_genres]
    }, 200


@books_bp.get("/month", responses={"200": BookViewSchema, "404": ErrorSchema})
def book_of_month():
    """Retorna o livro lido no mês atual

    Retorna uma representação do livro do mês.
    """
    logger.debug("Buscando livro do mês")
    session = Session()
    today = datetime.now()

    book = session.query(Book).filter(
        Book.read_date >= datetime(today.year, today.month, 1),
        Book.read_date < datetime(today.year, today.month + 1, 1) if today.month < 12
        else datetime(today.year + 1, 1, 1)
    ).first()

    if not book:
        session.close()
        error_msg = "Nenhum livro registrado para o mês atual :/"
        logger.warning(error_msg)
        return {"message": error_msg}, 404

    logger.debug(f"Livro do mês encontrado: '{book.title}'")
    result = apresenta_book(book)
    session.close()
    return result, 200