from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from model.base import Base


class Rating(Base):
    __tablename__ = "ratings"

    id = Column("pk_rating", Integer, primary_key=True, autoincrement=True)
    stars = Column(Integer, nullable=False)  # 0 a 5
    created_at = Column(DateTime, default=datetime.now())

    book_id = Column(Integer, ForeignKey("books.pk_book"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.pk_member"), nullable=False)

    book = relationship("Book", back_populates="ratings")
    member = relationship("Member", back_populates="ratings")

    # Um membro não pode avaliar o mesmo livro duas vezes
    __table_args__ = (
        UniqueConstraint("book_id", "member_id", name="uq_book_member"),
    )

    def __init__(self, book_id: int, member_id: int, stars: int):
        """
        Cria uma Rating (avaliação de um livro por um membro)

        Arguments:
            book_id: id do livro avaliado
            member_id: id do membro que avaliou
            stars: nota de 0 a 5
        """
        self.book_id = book_id
        self.member_id = member_id
        self.stars = stars