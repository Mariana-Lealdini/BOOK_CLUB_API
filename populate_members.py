import sys
import os

# Garante que o projeto está no path
sys.path.insert(0, os.path.dirname(__file__))

from model import Session
from model.member import Member

members = [
    "Mariana",
    "Tiffany",
    "Bruna",
    "Beatriz O.",
    "Maria",
    "Rebeca",
    "Sara",
    "Shirley",
    "Thalita",
    "Ana Beatriz",
    "Bianca L.",
    "Kamyla",
    "Ana Júlia",
    "Nicole",
    "Natalia",
    "Bianca B.",
    "Beatriz M.",
]

session = Session()

cadastrados = 0
ignorados   = 0

for name in members:
    exists = session.query(Member).filter(Member.name == name).first()
    if exists:
        print(f"  [ignorado] {name} — já cadastrada")
        ignorados += 1
        continue

    member = Member(name=name)
    session.add(member)
    print(f"  [ok] {name}")
    cadastrados += 1

session.commit()
session.close()

print(f"\n✓ {cadastrados} membras cadastradas, {ignorados} ignoradas.")