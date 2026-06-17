from flask_openapi3 import APIBlueprint, Tag

from model import Session
from model.member import Member
from logger import logger

from schemas import (
    MemberViewSchema,
    MemberListSchema,
    apresenta_members,
)

members_tag = Tag(name="Members", description="Busca de membros do clube")

members_bp = APIBlueprint(
    "members",
    __name__,
    url_prefix="/members",
    abp_tags=[members_tag]
)


@members_bp.get("/", responses={"200": MemberListSchema})
def get_members():
    """Retorna todos os membros cadastrados"""
    logger.debug("Coletando membros")
    session = Session()
    members = session.query(Member).all()
    result = apresenta_members(members)
    session.close()

    if not members:
        return {"members": []}, 200

    logger.debug(f"{len(members)} membros encontrados")
    return result, 200