import json
import fastapi
import os
import utils
import pydantic
import psycopg2

postgree_user = os.getenv("P_USER")
postgree_password = os.getenv("P_PASSWORD")
arg_char = "?"

if not postgree_user or not postgree_password:
    raise Exception("P_USER e P_PASSWORD precisa ser definido no ambiente.")

config = json.load(open("config.json"))
app_config = config["app"]
db_config = config["database"]
database = utils.get_connection(db_config, postgree_user, postgree_password)

app = fastapi.FastAPI(
    title="OldSchool",
    servers=[{"url": f"{app_config['url']}"}]
)

class UserCreate(pydantic.BaseModel):
    apelido: str
    link_avatar: pydantic.HttpUrl
    senha: str


@app.get("/")
async def root():
    if database:
        return {"status": "OK"}
    else:
        raise fastapi.HTTPException(status_code=500, detail="Database connection error")


@app.post("/usuarios")
async def create_user(user: UserCreate):
    if database:
        # Sanitização
        if not utils.validate(user.apelido, "username"):
             raise fastapi.HTTPException(status_code=400, detail="Formato invalido de usuário.")

        password_hash = utils.generate_hash(user.senha)
        
        try:
            query = f"INSERT INTO usuarios (apelido, link_avatar, hash_senha) VALUES (%s, %s, %s) RETURNING id;"
            result = utils.query(database, query, (user.apelido, str(user.link_avatar), password_hash))
        except psycopg2.errors.UniqueViolation:
            raise fastapi.HTTPException(status_code=400, detail="Um usuário com esse apelido ja existe.")

        if result is not None:
            return {"status": "OK",
                    "user_id": result[0]}
        else:
            raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    else:
        raise fastapi.HTTPException(status_code=500, detail="Database connection error")
