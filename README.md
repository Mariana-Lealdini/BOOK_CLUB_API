# Book Club API

Este projeto tem como objetivo o gerenciamento do histórico de leituras do **The Book Lovers Club** (Clube do Livro Feminino).
Permite cadastrar, buscar, filtrar e remover livros, registrar avaliações com
estrelas por membro, e exibir estatísticas de leitura do clube.

---

## Como executar

Será necessário ter todas as libs Python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).


**1. Instale as dependências:**
Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

```
(env)$ pip install -r requirements.txt
```

**2. Popule os membros do clube (apenas na primeira execução, ou caso mais membros sejam adicionados):**
Este comando popula os membros do clube no banco de dados e deve ser utilizado na primeira execução 
ou em caso de adições de membros a "populate_member.py".

```
(env)$ python populate_members.py
```

**3. Execute a API:**
```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor 
automaticamente após uma mudança no código fonte. 
```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

---

## Acesso à documentação

Abra o endereço abaixo no navegador para acessar a documentação interativa (Swagger):

http://localhost:5000/openapi

---


## Membros do clube

Os membros são cadastrados via script na primeira execução. O gerenciamento
de membros é feito exclusivamente pelo script `populate_member.py`, sem
exposição de rotas de cadastro ou remoção. No frontend, os membros aparecem
como lista suspensa para seleção na avaliação/recomendação de livros.

---

## Arquitetura

O projeto segue uma arquitetura em camadas baseada no padrão MVC adaptado
para APIs REST:

- **`model/`** — mapeamento objeto-relacional via SQLAlchemy, definindo as
entidades do domínio e seus relacionamentos com o banco de dados
- **`schemas/`** — contratos de entrada e saída da API usando Pydantic,
responsáveis pela validação e serialização dos dados
- **`routes/`** — controllers que recebem as requisições HTTP, orquestram
a lógica de negócio e retornam as respostas adequadas

---

## Tecnologias utilizadas

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Flask-OpenAPI3](https://luolingchun.github.io/flask-openapi3/) — documentação Swagger automática
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM para banco de dados
- [SQLite](https://www.sqlite.org/) — banco de dados local
- [Pydantic](https://docs.pydantic.dev/) — validação de dados
