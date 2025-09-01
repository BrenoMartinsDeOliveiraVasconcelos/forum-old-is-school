import json
import fastapi
import os
import utils
import classes
import auth
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

postgree_user = os.getenv("P_USER")
postgree_password = os.getenv("P_PASSWORD")

if not postgree_user or not postgree_password:
    raise Exception("P_USER e P_PASSWORD precisa ser definido no ambiente.")

config = json.load(open("config.json", encoding='utf-8'))
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


@app.post("/token", tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = fastapi.Depends()):
    authenticated = utils.authenticate(database, form_data.username, form_data.password)
    if not authenticated:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES_INT) 

    access_token = auth.create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/usuarios")
async def create_user(user: classes.UserCreate):
    # Sanitização
    if not utils.validate(user.apelido, "username"):
            raise fastapi.HTTPException(status_code=400, detail="Formato invalido de usuário.")

    password_hash = utils.generate_hash(user.senha)
    
    result = utils.insert_into(database, "usuarios", ["apelido", "link_avatar", "hash_senha"], [user.apelido, str(user.link_avatar), password_hash], "id")

    if result:
        return {"user_id": result[0]} #type: ignore
    elif result is None:
        raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    elif result is False:
        raise fastapi.HTTPException(status_code=409, detail="Usuário ja cadastrado")
    

@app.post("/posts")
async def publish(info: classes.Publish, current_user_apelido: str = fastapi.Depends(auth.get_current_user)):
    autor_id = utils.get_user_id(database, current_user_apelido)

    if not autor_id:
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
async def comment(info: classes.Comment, current_user_apelido: str = fastapi.Depends(auth.get_current_user)):
    autor_id = utils.get_user_id(database, current_user_apelido)

    if not autor_id:
        raise fastapi.HTTPException(status_code=401, detail="Acesso negado")
    
    if not utils.check_existence(database, "posts", "id", str(info.post_id)):
        raise fastapi.HTTPException(status_code=404, detail="Post nao encontrado")

    result = utils.insert_into(database, "comentarios", ["autor_id", "post_id", "conteudo"], [autor_id, info.post_id, info.conteudo], "id")

    if result:
        return {"comment_id": result[0]} #type: ignore
    else:
        raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    

@app.post("/mensagens")
async def send_message(info: classes.SendMessage, current_user_apelido: str = fastapi.Depends(auth.get_current_user)):
    autor_id = utils.get_user_id(database, current_user_apelido)

    if not autor_id:
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
    posts = utils.select_where(database, str(post_id), "id", "posts", ["id", "autor_id", "titulo", "conteudo", "timestamp"])
    
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
    str_user_id = str(user_id)

    users = utils.select_where(database, str_user_id, "id", "usuarios", ["id", "apelido", "link_avatar"])
    
    if not users:
        raise fastapi.HTTPException(status_code=404, detail="Usuário nao encontrado")

    for user in users["usuarios"]:
        user["posts"] = utils.select_where(database, str_user_id, "autor_id", "posts", ["id", "autor_id", "titulo", "conteudo", "timestamp"])
        user["mensagens"] = utils.select_where(database, str_user_id, "autor_id", "mensagens", ["id", "autor_id", "mensagem", "timestamp"])
        user["comentarios"] = utils.select_where(database, str_user_id, "autor_id", "comentarios", ["id", "autor_id", "post_id", "conteudo", "timestamp"])
    return users


@app.get("/comentarios/{comentario_id}")
async def get_comment(comentario_id: int):
    comentarios = utils.select_where(database, str(comentario_id), "id", "comentarios", ["id", "autor_id", "post_id", "conteudo", "timestamp"])
    
    if not comentarios:
        raise fastapi.HTTPException(status_code=404, detail="Comentario nao encontrado")
    
    for comentario in comentarios["comentarios"]:
        comentario["post_titulo"] = utils.select_where(database, comentario["post_id"], "id", "posts", ["titulo"])["posts"][0]["titulo"]
        comentario["autor"] = utils.select_where(database, comentario["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]

    return comentarios


@app.get("/mensagens/{mensagem_id}")
async def get_msg(mensagem_id: int):
    mensagens = utils.select_where(database, str(mensagem_id), "id", "mensagens", ["id", "autor_id", "mensagem", "timestamp"])
    
    if not mensagens:
        raise fastapi.HTTPException(status_code=404, detail="Mensagem nao encontrada")
    
    for mensagem in mensagens["mensagens"]:
        mensagem["autor"] = utils.select_where(database, mensagem["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]

    return mensagens


# Conseguir do usuário cada coisa

@app.get("/usuarios/{user_id}/posts")
async def get_user_posts(user_id: int):
    return utils.select_where(database, str(user_id), "autor_id", "posts", ["id", "autor_id", "titulo", "conteudo", "timestamp"])


@app.get("/usuarios/{user_id}/comentarios")
async def get_user_comments(user_id: int):
    return utils.select_where(database, str(user_id), "autor_id", "comentarios", ["id", "autor_id", "post_id", "conteudo", "timestamp"])


@app.get("/usuarios/{user_id}/mensagens")
async def get_user_messages(user_id: int):
    return utils.select_where(database, str(user_id), "autor_id", "mensagens", ["id", "autor_id", "mensagem", "timestamp"])


# Edição de perfil e afins

@app.post("/usuarios/{user_id}/editar/avatar")
async def edit_avatar(link_avatar: classes.Avatar, user_id: int, current_user_apelido: str = fastapi.Depends(auth.get_current_user)):
    logged_id = utils.get_user_id(database, current_user_apelido)

    if logged_id != user_id:
        raise fastapi.HTTPException(status_code=401, detail="Acesso negado")

    update = utils.update_data(database, "usuarios", "link_avatar", "id", str(user_id), str(link_avatar.link_avatar))    

    if not update:
        raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    
    return {"status": "OK"}


@app.post("/usuarios/{user_id}/editar/biografia")
async def edit_bio(bio: classes.Bio, user_id: int, current_user_apelido: str = fastapi.Depends(auth.get_current_user)):
    logged_id = utils.get_user_id(database, current_user_apelido)

    if logged_id != user_id:
        raise fastapi.HTTPException(status_code=401, detail="Acesso negado")

    update = utils.update_data(database, "usuarios", "biografia", "id", str(user_id), str(bio.texto))    

    if not update:
        raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    
    return {"status": "OK"}
