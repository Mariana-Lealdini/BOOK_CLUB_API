from pydantic import BaseModel
from typing import List
from model.member import Member


class MemberViewSchema(BaseModel):
    """Define como um membro será retornado"""
    id: int = 1
    name: str = "Mariana"


class MemberListSchema(BaseModel):
    """Define como uma listagem de membros será retornada"""
    members: List[MemberViewSchema]


def apresenta_members(members: List[Member]):
    """Retorna uma representação da listagem de membros"""
    return {"members": [{"id": m.id, "name": m.name} for m in members]}