from sqlalchemy import Column, String, Integer, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from model.base import Base


class Book(Base):
    __tablename__ = "books"

    id = Column("pk_book", Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    author = Column(String(150), nullable=False)
    genre = Column(String(100), nullable=False)
    read_date = Column(DateTime, nullable=False)
    recommended_by = Column(String(150), nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    ratings = relationship("Rating", back_populates="book", cascade="all, delete-orphan")

    # Dois livros não podem ter o mesmo título E o mesmo autor.
    # Livros homônimos de autores diferentes são permitidos.
    __table_args__ = (
        UniqueConstraint("title", "author", name="uq_book_title_author"),
    )

    def __init__(self, title: str, author: str, genre: str,
                 read_date: Union[DateTime, None] = None,
                 recommended_by: str = ""):
        """
        Cria um Book (livro lido pelo clube do livro)

        Arguments:
            title: título do livro
            author: nome do autor do livro
            genre: gênero literário do livro
            read_date: mês e ano em que o livro foi lido pelo clube
            recommended_by: nome de quem indicou o livro
        """
        self.title = title
        self.author = author
        self.genre = genre
        self.recommended_by = recommended_by

        if read_date:
            self.read_date = read_date
        else:
            today = datetime.now()
            self.read_date = datetime(today.year, today.month, 1)