import json
import fastapi
import os
import utils
import classes

postgree_user = os.getenv("P_USER")
postgree_password = os.getenv("P_PASSWORD")
arg_char = "?"

if not postgree_user or not postgree_password:
    raise Exception("P_USER e P_PASSWORD precisa ser definido no ambiente.")

config = json.load(open("config.json"))
db_config = config["database"]
database = utils.get_connection(db_config, postgree_user, postgree_password)

if not database:
    raise Exception("Database connection error")

app = fastapi.FastAPI(
    title="OldSchool"
)


@app.get("/")
async def root():
    if database:
        return {"status": "OK"}
    else:
        raise fastapi.HTTPException(status_code=500, detail="Database connection error")


@app.post("/usuarios")
async def create_user(user: classes.UserCreate):
    # Sanitização
    if not utils.validate(user.apelido, "username"):
            raise fastapi.HTTPException(status_code=400, detail="Formato invalido de usuário.")

    password_hash = utils.generate_hash(user.senha)
    
    query = f"INSERT INTO usuarios (apelido, link_avatar, hash_senha) VALUES (%s, %s, %s) RETURNING id;"
    result = utils.query(database, query, (user.apelido, str(user.link_avatar), password_hash))

    if result:
        return {"user_id": result[0]}
    elif result is None:
        raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    elif result is False:
        raise fastapi.HTTPException(status_code=409, detail="Usuário ja cadastrado")
    

@app.post("/posts")
async def publish(info: classes.Publish):
    authenticated = utils.authenticate(database, info.autor_apelido, info.senha)

    if not authenticated:
        raise fastapi.HTTPException(status_code=401, detail="Acesso negado")
    
    query = f"INSERT INTO posts (autor_id, titulo, conteudo, timestamp) VALUES (%s, %s, %s, NOW()) RETURNING id;"
    result = utils.query(database, query, (info.autor_id, info.titulo, info.conteudo))

    if result:
        if isinstance(result, tuple):
            return {"post_id": result[0]}
        elif isinstance(result, int):
            if utils.ERROR_CODES["TOO_LONG"] == result:
                raise fastapi.HTTPException(status_code=400, detail="Conteudo muito longo")
    else:
        raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    

@app.post("/comentarios")
async def comment(info: classes.Comment):
    authenticated = utils.authenticate(database, info.autor_apelido, info.senha)

    if not authenticated:
        raise fastapi.HTTPException(status_code=401, detail="Acesso negado")
    
    query = "INSERT INTO comentarios (autor_id, post_id, conteudo, timestamp) VALUES (%s, %s, %s, NOW()) RETURNING id;"
    result = utils.query(database, query, (info.autor_id, info.post_id, info.conteudo))

    if result:
        return {"comment_id": result[0]}
    else:
        raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    

@app.post("/mensagens")
async def send_message(info: classes.SendMessage):
    authenticated = utils.authenticate(database, info.autor_apelido, info.senha)

    if not authenticated:
        raise fastapi.HTTPException(status_code=401, detail="Acesso negado")
    
    query = "INSERT INTO mensagens (autor_id, mensagem, timestamp) VALUES (%s, %s, NOW()) RETURNING id;"
    result = utils.query(database, query, (info.autor_id, info.mensagem))

    if result:
        if isinstance(result, tuple):
            return {"message_id": result[0]}
        else:
            raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    else:
        raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    

# Métodos GET que pegam todos de cada categoria

@app.get("/usuarios")
async def get_users():
    return utils.select_all(database, ["id", "apelido", "link_avatar"], "usuarios")


@app.get("/posts")
async def get_posts():
    posts = utils.select_all(database, ["id", "autor_id", "titulo", "conteudo", "timestamp"], "posts")
    comentarios = utils.select_all(database, ["id", "autor_id", "post_id", "conteudo", "timestamp"], "comentarios")
    usuarios = utils.select_all(database, ["id", "apelido", "link_avatar"], "usuarios")

    for post in posts["posts"]:
        post["comentarios"] = []
        for comentario in comentarios["comentarios"]:
            if post["id"] == comentario["post_id"]:
                post["comentarios"].append(comentario)
        for user in usuarios["usuarios"]:
            if post["autor_id"] == user["id"]:
                post["autor"] = user["apelido"]

    return posts

    
@app.get("/mensagens")
async def get_messages():
    mensagens = utils.select_all(database, ["id", "autor_id", "mensagem", "timestamp"], "mensagens")
    usuarios = utils.select_all(database, ["id", "apelido", "link_avatar"], "usuarios")

    for mensagem in mensagens["mensagens"]:
        for user in usuarios["usuarios"]:
            if mensagem["autor_id"] == user["id"]:
                mensagem["autor"] = user["apelido"]

    return mensagens

