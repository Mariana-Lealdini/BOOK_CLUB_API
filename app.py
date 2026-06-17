from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_cors import CORS

from logger import logger
from schemas import *

from routes.books import books_bp
from routes.members import members_bp
from routes.ratings import ratings_bp

info = Info(title="Book Club API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')

app.register_api(books_bp)
app.register_api(members_bp)
app.register_api(ratings_bp)

if __name__ == "__main__":
    app.run(debug=True)