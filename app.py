import json
import fastapi
import psycopg2
import os
import utils
import pydantic

postgree_user = os.getenv("P_USER")
postgree_password = os.getenv("P_PASSWORD")
arg_char = "?"

if not postgree_user or not postgree_password:
    raise Exception("P_USER e P_PASSWORD precisa ser definido no ambiente.")

config = json.load(open("config.json"))
app_config = config["app"]
db_config = config["database"]

app = fastapi.FastAPI(
    title="OldSchool",
    servers=[{"url": f"{app_config['url']}"}]
)

class User(pydantic.BaseModel):
    apelido: str
    link_avatar: pydantic.HttpUrl
    senha: str


def get_connection():
    return psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        database=db_config["name"],
        user=postgree_user,
        password=postgree_password
    )

@app.get("/")
async def root():
    database = get_connection()

    if database:
        database.close()
        return {"status": "OK"}
    else:
        raise fastapi.HTTPException(status_code=500, detail="Database connection error")


@app.post("/usuarios")
async def create_user(user: User):
    database = get_connection()

    if database:
        cursor = database.cursor()

        # Sanitização
        if not utils.validate(user.apelido, "username"):
             raise fastapi.HTTPException(status_code=400, detail="Formato invalido de usuário.")

        password_hash = utils.generate_hash(user.senha)
        query = f"INSERT INTO usuarios (apelido, link_avatar, hash_senha) VALUES (%s, %s, %s);"

        cursor.execute(query, (user.apelido, str(user.link_avatar), password_hash))
        database.commit()
        cursor.close()
        database.close()
        return {"status": "OK"}
    else:
        raise fastapi.HTTPException(status_code=500, detail="Database connection error")
