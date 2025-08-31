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
    
    result = utils.insert_into(database, "usuarios", ["apelido", "link_avatar", "hash_senha"], [user.apelido, str(user.link_avatar), password_hash], "id")

    if result:
        return {"user_id": result[0]}
    elif result is None:
        raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    elif result is False:
        raise fastapi.HTTPException(status_code=409, detail="Usuário ja cadastrado")
    

@app.post("/posts")
async def publish(info: classes.Publish):
    authenticated = utils.authenticate(database, info.autor_apelido, info.senha)
    autor_id = utils.get_user_id(database, info.autor_apelido)

    if not authenticated or not autor_id:
        raise fastapi.HTTPException(status_code=401, detail="Acesso negado")
    
    result = utils.insert_into(database, "posts", ["autor_id", "titulo", "conteudo"], [autor_id, info.titulo, info.conteudo], "id")

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
    autor_id = utils.get_user_id(database, info.autor_apelido)

    if not authenticated or not autor_id:
        raise fastapi.HTTPException(status_code=401, detail="Acesso negado")
    
    if not utils.check_existence(database, "posts", "id", info.post_id):
        raise fastapi.HTTPException(status_code=404, detail="Post nao encontrado")

    result = utils.insert_into(database, "comentarios", ["autor_id", "post_id", "conteudo"], [autor_id, info.post_id, info.conteudo], "id")

    if result:
        return {"comment_id": result[0]}
    else:
        raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    

@app.post("/mensagens")
async def send_message(info: classes.SendMessage):
    authenticated = utils.authenticate(database, info.autor_apelido, info.senha)
    autor_id = utils.get_user_id(database, info.autor_apelido)

    if not authenticated or not autor_id:
        raise fastapi.HTTPException(status_code=401, detail="Acesso negado")
    
    #query = "INSERT INTO mensagens (autor_id, mensagem, timestamp) VALUES (%s, %s, NOW()) RETURNING id;"
    #result = utils.query(database, query, (autor_id, info.mensagem))

    result = utils.insert_into(database, "mensagens", ["autor_id", "mensagem"], [autor_id, info.mensagem], "id")

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

    for post in posts["posts"]:
        post["comentarios"] = []
        post["autor"] = utils.select_where(database, post["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]
        comentarios = utils.select_where(database, post["id"], "post_id", "comentarios", ["id", "autor_id", "post_id", "conteudo", "timestamp"])
        
        if comentarios:
            for comentario in comentarios["comentarios"]:
                if post["id"] == comentario["post_id"]:
                    comentario["autor"] = utils.select_where(database, comentario["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]
                    post["comentarios"].append(comentario)

    return posts

    
@app.get("/mensagens")
async def get_messages():
    mensagens = utils.select_all(database, ["id", "autor_id", "mensagem", "timestamp"], "mensagens")
    
    for mensagem in mensagens["mensagens"]:
        mensagem["autor"] = utils.select_where(database, mensagem["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]
    return mensagens



@app.get("/comentarios")
async def get_comments():
    comentarios = utils.select_all(database, ["id", "autor_id", "post_id", "conteudo", "timestamp"], "comentarios")

    for comentario in comentarios["comentarios"]:
        comentario["post_titulo"] = utils.select_where(database, comentario["post_id"], "id", "posts", ["titulo"])["posts"][0]["titulo"]
        comentario["autor"] = utils.select_where(database, comentario["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]
    return comentarios

# Posts por id
@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    posts = utils.select_where(database, post_id, "id", "posts", ["id", "autor_id", "titulo", "conteudo", "timestamp"])
    
    if not posts:
        raise fastapi.HTTPException(status_code=404, detail="Post nao encontrado")
    
    for post in posts["posts"]:
        post["comentarios"] = []
        comentarios = utils.select_where(database, post["id"], "post_id", "comentarios", ["id", "autor_id", "post_id", "conteudo", "timestamp"])
        
        if comentarios:
            for comentario in comentarios["comentarios"]:
                if post["id"] == comentario["post_id"]:
                    comentario["autor"] = utils.select_where(database, comentario["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]
                    post["comentarios"].append(comentario)

    return posts


# Tudo relacionado ao usuário
@app.get("/usuarios/{user_id}")
async def get_user_content(user_id: int):
    users = utils.select_where(database, user_id, "id", "usuarios", ["id", "apelido", "link_avatar"])
    
    if not users:
        raise fastapi.HTTPException(status_code=404, detail="Usuário nao encontrado")

    for user in users["usuarios"]:
        user["posts"] = utils.select_where(database, user_id, "autor_id", "posts", ["id", "autor_id", "titulo", "conteudo", "timestamp"])
        user["mensagens"] = utils.select_where(database, user_id, "autor_id", "mensagens", ["id", "autor_id", "mensagem", "timestamp"])
        user["comentarios"] = utils.select_where(database, user_id, "autor_id", "comentarios", ["id", "autor_id", "post_id", "conteudo", "timestamp"])
    return users


@app.get("/comentarios/{comentario_id}")
async def get_comment(comentario_id: int):
    comentarios = utils.select_where(database, comentario_id, "id", "comentarios", ["id", "autor_id", "post_id", "conteudo", "timestamp"])
    
    if not comentarios:
        raise fastapi.HTTPException(status_code=404, detail="Comentario nao encontrado")
    
    for comentario in comentarios["comentarios"]:
        comentario["post_titulo"] = utils.select_where(database, comentario["post_id"], "id", "posts", ["titulo"])["posts"][0]["titulo"]
        comentario["autor"] = utils.select_where(database, comentario["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]

    return comentarios


@app.get("/mensagens/{mensagem_id}")
async def get_msg(mensagem_id: int):
    mensagens = utils.select_where(database, mensagem_id, "id", "mensagens", ["id", "autor_id", "mensagem", "timestamp"])
    
    if not mensagens:
        raise fastapi.HTTPException(status_code=404, detail="Mensagem nao encontrada")
    
    for mensagem in mensagens["mensagens"]:
        mensagem["autor"] = utils.select_where(database, mensagem["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]

    return mensagens


# Conseguir do usuário cada coisa

@app.get("/usuarios/{user_id}/posts")
async def get_user_posts(user_id: int):
    return utils.select_where(database, user_id, "autor_id", "posts", ["id", "autor_id", "titulo", "conteudo", "timestamp"])


@app.get("/usuarios/{user_id}/comentarios")
async def get_user_comments(user_id: int):
    return utils.select_where(database, user_id, "autor_id", "comentarios", ["id", "autor_id", "post_id", "conteudo", "timestamp"])


@app.get("/usuarios/{user_id}/mensagens")
async def get_user_messages(user_id: int):
    return utils.select_where(database, user_id, "autor_id", "mensagens", ["id", "autor_id", "mensagem", "timestamp"])