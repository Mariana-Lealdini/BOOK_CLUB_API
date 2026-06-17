from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from model.base import Base


class Member(Base):
    __tablename__ = "members"

    id = Column("pk_member", Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now())

    ratings = relationship("Rating", back_populates="member")

    def __init__(self, name: str):
        """
        Cria um Member (membro do clube do livro)

        Arguments:
            name: nome da membra
        """
        self.name = name