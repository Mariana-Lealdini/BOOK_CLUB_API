from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from model import Session
from model.rating import Rating
from model.books import Book
from model.member import Member
from logger import logger

from schemas import (
    RatingSchema,
    RatingBuscaSchema,  # ← adicionar essa linha
    RatingViewSchema,
    RatingListSchema,
    ErrorSchema,
    apresenta_rating,
    apresenta_ratings,
)

ratings_tag = Tag(name="Ratings", description="Avaliações de livros por membros do clube")

ratings_bp = APIBlueprint(
    "ratings",
    __name__,
    url_prefix="/ratings",
    abp_tags=[ratings_tag]
)


@ratings_bp.post("/", responses={"200": RatingViewSchema, "409": ErrorSchema, "404": ErrorSchema, "400": ErrorSchema})
def add_rating(body: RatingSchema):
    """Registra a avaliação de um livro por um membro"""
    logger.debug(f"Registrando avaliação — membro: {body.member_id}, livro: {body.book_id}")
    
    try:
        session = Session()

        # Verifica se livro existe
        book = session.query(Book).filter(Book.id == body.book_id).first()
        if not book:
            return {"message": "Livro não encontrado :/"}, 404

        # Verifica se membro existe
        member = session.query(Member).filter(Member.id == body.member_id).first()
        if not member:
            return {"message": "Membro não encontrado :/"}, 404

        rating = Rating(
            book_id=body.book_id,
            member_id=body.member_id,
            stars=body.stars
        )
        session.add(rating)
        session.commit()
        logger.debug(f"Avaliação registrada: livro '{book.title}' por '{member.name}'")
        return apresenta_rating(rating, book, member), 200

    except IntegrityError:
        error_msg = "Este membro já avaliou este livro :/"
        logger.warning(f"Avaliação duplicada — membro {body.member_id}, livro {body.book_id}")
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível registrar a avaliação :/"
        logger.warning(f"Erro ao registrar avaliação: {e}")
        return {"message": error_msg}, 400


@ratings_bp.get("/", responses={"200": RatingListSchema})
def get_ratings():
    """Retorna todas as avaliações"""
    logger.debug("Coletando avaliações")
    session = Session()

    ratings = session.query(Rating).options(
        joinedload(Rating.book),
        joinedload(Rating.member)
    ).all()

    session.close()

    if not ratings:
        return {"ratings": []}, 200

    return apresenta_ratings(ratings), 200


@ratings_bp.get("/book", responses={"200": RatingListSchema, "404": ErrorSchema})
def get_ratings_by_book(query: RatingBuscaSchema):
    """Retorna todas as avaliações de um livro específico"""
    logger.debug(f"Buscando avaliações do livro id: {query.book_id}")
    session = Session()

    book = session.query(Book).filter(Book.id == query.book_id).first()
    if not book:
        return {"message": "Livro não encontrado :/"}, 404

    ratings = session.query(Rating).options(
        joinedload(Rating.book),
        joinedload(Rating.member)
    ).filter(Rating.book_id == query.book_id).all()
    session.close()

    return apresenta_ratings(ratings), 200