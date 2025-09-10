import json
import fastapi
from fastapi import UploadFile, Header, File
import os
import utils
import classes
import auth
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, FileResponse
from datetime import timedelta
from typing import Annotated

postgree_user = os.getenv("P_USER")
postgree_password = os.getenv("P_PASSWORD")

if not postgree_user or not postgree_password:
    raise Exception("P_USER e P_PASSWORD precisa ser definido no ambiente.")

config = json.load(open("config.json", encoding='utf-8'))
db_config = config["database"]
database = utils.get_connection(db_config, postgree_user, postgree_password)

if not database:
    raise Exception("Database connection error")

app_conifg = config["app"]
deletion = app_conifg["text_on_deletion"]

app = fastapi.FastAPI(
    title="OldSchool"
)

headers = {"Access-Control-Allow-Origin": "*"}


# Image folder
absoulute_path = app_conifg["data_path"]
image_folder = os.path.join(absoulute_path, "images")
avatar_folder = os.path.join(image_folder, "avatars")
media_folder = os.path.join(absoulute_path, "media")
os.makedirs(image_folder, exist_ok=True)
os.makedirs(avatar_folder, exist_ok=True)
os.makedirs(media_folder, exist_ok=True)


supported_image_types = ["jpg", "jpeg", "png", "gif"]


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

    j = {"access_token": access_token, "token_type": "bearer"}

    return JSONResponse(content=j, headers=headers)


@app.post("/usuarios")
async def create_user(user: classes.UserCreate):
    # Sanitização
    if not utils.validate(user.apelido, "username"):
            raise fastapi.HTTPException(status_code=400, detail="Formato invalido de usuário.")

    password_hash = utils.generate_hash(user.senha)
    
    result = utils.insert_into(database, "usuarios", ["apelido", "hash_senha"], [user.apelido, password_hash], "id")

    j = {"user_id": result[0]}

    return JSONResponse(content=j, headers=headers) #type: ignore
    

@app.post("/posts")
async def publish(info: classes.Publish, current_user_apelido: str = fastapi.Depends(auth.get_current_user)):
    autor_id = utils.get_user_id(database, current_user_apelido)
    assinatura = utils.select_where(database, autor_id, "id", "usuarios", ["assinatura"])["usuarios"][0]["assinatura"]

    print(assinatura)

    if assinatura:
        info.conteudo += "\n\n" + assinatura

    utils.check_existence(database, "categorias", "id", str(info.categoria_id))
    
    result = utils.insert_into(database, "posts", ["autor_id", "titulo", "conteudo", "categoria_id"], [autor_id, info.titulo, info.conteudo, info.categoria_id], "id")

    j = {"post_id": result[0]}

    return JSONResponse(content=j, headers=headers)

@app.post("/mural")
async def publish_with_media(titulo: str, conteudo: str, file: UploadFile = File(...), current_user_apelido: str = fastapi.Depends(auth.get_current_user)):
    autor_id = utils.get_user_id(database, current_user_apelido)
    assinatura = utils.select_where(database, autor_id, "id", "usuarios", ["assinatura"])["usuarios"][0]["assinatura"]

    if assinatura:
        conteudo += "\n\n" + assinatura

    caminho_arquivo = os.path.join(media_folder, file.filename)
    with open(caminho_arquivo, "wb+") as buffer:
        buffer.write(file.file.read())

    result = utils.insert_into(database, "posts", ["autor_id", "titulo", "conteudo", "midia", "mural"], [autor_id, titulo, conteudo, file.filename, "true"], "id")

    j = {"post_id": result[0]}

    return JSONResponse(content=j, headers=headers)


@app.post("/comentarios")
async def comment(info: classes.Comment, current_user_apelido: str = fastapi.Depends(auth.get_current_user)):
    autor_id = utils.get_user_id(database, current_user_apelido)
    assinatura = utils.select_where(database, autor_id, "id", "usuarios", ["assinatura"])["usuarios"][0]["assinatura"]

    if assinatura:
        info.conteudo += "\n\n" + assinatura

    utils.check_existence(database, "posts", "id", str(info.post_id))

    result = utils.insert_into(database, "comentarios", ["autor_id", "post_id", "conteudo"], [autor_id, info.post_id, info.conteudo], "id")
    
    j = {"comment_id": result[0]}
    return JSONResponse(content=j, headers=headers)
    

@app.post("/mensagens")
async def send_message(info: classes.SendMessage, current_user_apelido: str = fastapi.Depends(auth.get_current_user)):
    autor_id = utils.get_user_id(database, current_user_apelido)
    
    #query = "INSERT INTO mensagens (autor_id, mensagem, timestamp) VALUES (%s, %s, NOW()) RETURNING id;"
    #result = utils.query(database, query, (autor_id, info.mensagem))

    result = utils.insert_into(database, "mensagens", ["autor_id", "mensagem"], [autor_id, info.mensagem], "id")
    j = {"message_id": result[0]}
    return JSONResponse(content=j, headers=headers)



@app.post("/categorias")
async def create_category(category: classes.Category, current_user_apelido: str = fastapi.Depends(auth.get_current_user)):
    user_id = utils.get_user_id(database, current_user_apelido)
    utils.check_privileges(database, user_id)

    result = utils.insert_into(database, "categorias", ["titulo", "desc"], [category.titulo, category.desc], "id")
    j = {"category_id": result[0]}
    return JSONResponse(content=j, headers=headers)


# Métodos GET que pegam todos de cada categoria

@app.get("/usuarios")
async def get_users(paging: classes.Paging):
    #j = utils.select_all(database, ["id", "apelido", "avatar_filename", "deletado"], "usuarios", paging.page, paging.page_size)
    
    j = utils.select_all(
        database,
        ["id", "apelido", "avatar_filename", "assinatura", "admin", "deletado"],
        "usuarios",
        paging.page,
        paging.page_size
    )
    return JSONResponse(content=j, headers=headers)


@app.get("/posts")
async def get_posts(paging: classes.PagingPosts):
    posts = utils.select_all(database, ["id", "autor_id", "titulo", "conteudo", "midia", "mural", "categoria_id", "timestamp"], "posts", paging.page, paging.page_size, where=True, condition_column="categoria_id", condition_value=str(paging.categoria_id))

    for post in posts["posts"]:
        post["comentarios"] = []
        post["autor"] = utils.select_where(database, post["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]
        comentarios = utils.select_where(database, post["id"], "post_id", "comentarios", ["id", "autor_id", "post_id", "conteudo", "timestamp"])
        
        if comentarios:
            for comentario in comentarios["comentarios"]:
                if post["id"] == comentario["post_id"]:
                    comentario["autor"] = utils.select_where(database, comentario["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]
                    post["comentarios"].append(comentario)

    return JSONResponse(content=posts, headers=headers)

    
@app.get("/mensagens")
async def get_messages(paging: classes.Paging):
    mensagens = utils.select_all(database, ["id", "autor_id", "mensagem", "timestamp"], "mensagens", paging.page, paging.page_size)
    
    for mensagem in mensagens["mensagens"]:
        mensagem["autor"] = utils.select_where(database, mensagem["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]
    k = mensagens

    return JSONResponse(content=mensagens, headers=headers)



@app.get("/comentarios")
async def get_comments(paging: classes.Paging):
    comentarios = utils.select_all(database, ["id", "autor_id", "post_id", "conteudo", "timestamp"], "comentarios", paging.page, paging.page_size)

    for comentario in comentarios["comentarios"]:
        comentario["post_titulo"] = utils.select_where(database, comentario["post_id"], "id", "posts", ["titulo"])["posts"][0]["titulo"]
        comentario["autor"] = utils.select_where(database, comentario["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]
    return JSONResponse(content=comentarios, headers=headers)


@app.get("/categorias")
async def get_categories(paging: classes.Paging):
    categorias = utils.select_all(database, ["id", "titulo", "desc", "timestamp"], "categorias", paging.page, paging.page_size)
    return JSONResponse(content=categorias, headers=headers)

# Posts por id
@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    posts = utils.select_where(database, str(post_id), "id", "posts", ["id", "autor_id", "titulo", "conteudo", "midia", "mural", "categoria_id", "timestamp"], True)
    
    
    for post in posts["posts"]:
        post["comentarios"] = {"comentarios": []}
        comentarios = utils.select_all(
            connection=database,
            columns=["id", "autor_id", "post_id", "conteudo", "timestamp"],
            table="comentarios",
            page=1,
            page_size=100,
            where=True,
            condition_column="post_id",
            condition_value=str(post["id"])
        )

        if comentarios:
            for comentario in comentarios["comentarios"]:
                comentario["autor"] = utils.select_where(database, comentario["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]
                post["comentarios"]["comentarios"].append(comentario)

        post["comentarios"]["page"] = comentarios["page"]

    return JSONResponse(content=posts, headers=headers)


# Tudo relacionado ao usuário
@app.get("/usuarios/{user_id}")
async def get_user_content(user_id: int, paging: classes.Paging):
    str_user_id = str(user_id)

    users = utils.select_where(database, str_user_id, "id", "usuarios", ["id", "apelido", "avatar_filename", "assinatura", "admin"], True)
    

    for user in users["usuarios"]:
        user["posts"] = utils.select_all(
            connection=database,
            columns=["id", "autor_id", "titulo", "conteudo", "midia", "mural", "categoria_id", "timestamp"],
            table="posts",
            page=paging.page,
            page_size=paging.page_size,
            where=True,
            condition_column="autor_id",
            condition_value=str_user_id
        )

        user["mensagens"] = utils.select_all(
            connection=database,
            columns=["id", "autor_id", "mensagem", "timestamp"],
            table="mensagens",
            page=paging.page,
            page_size=paging.page_size,
            where=True,
            condition_column="autor_id",
            condition_value=str_user_id
        )

        user["comentarios"] = utils.select_all(
            connection=database,
            columns=["id", "autor_id", "post_id", "conteudo", "timestamp"],
            table="comentarios",
            page=paging.page,
            page_size=paging.page_size,
            where=True,
            condition_column="autor_id",
            condition_value=str_user_id
        )
    
    return JSONResponse(content=users, headers=headers)


@app.get("/comentarios/{comentario_id}")
async def get_comment(comentario_id: int):
    comentarios = utils.select_where(database, str(comentario_id), "id", "comentarios", ["id", "autor_id", "post_id", "conteudo", "timestamp"], True)
    
    
    for comentario in comentarios["comentarios"]:
        comentario["post_titulo"] = utils.select_where(database, comentario["post_id"], "id", "posts", ["titulo"])["posts"][0]["titulo"]
        comentario["autor"] = utils.select_where(database, comentario["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]

    return JSONResponse(content=comentarios, headers=headers)


@app.get("/mensagens/{mensagem_id}")
async def get_msg(mensagem_id: int):
    mensagens = utils.select_where(database, str(mensagem_id), "id", "mensagens", ["id", "autor_id", "mensagem", "timestamp"], True)
    
    for mensagem in mensagens["mensagens"]:
        mensagem["autor"] = utils.select_where(database, mensagem["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]

    return JSONResponse(content=mensagens, headers=headers)


# Conseguir do usuário cada coisa

@app.get("/usuarios/{user_id}/posts")
async def get_user_posts(user_id: int, paging: classes.Paging):
    #j = utils.select_where(database, str(user_id), "autor_id", "posts", ["id", "autor_id", "titulo", "conteudo", "timestamp"])
    j = utils.select_all(
        connection=database,
        columns=["id", "autor_id", "titulo", "conteudo", "midia", "mural", "categoria_id", "timestamp"],
        table="posts",
        page=paging.page,
        page_size=paging.page_size,
        where=True,
        condition_column="autor_id",
        condition_value=str(user_id)
    )

    return JSONResponse(content=j, headers=headers)


@app.get("/usuarios/{user_id}/comentarios")
async def get_user_comments(user_id: int, paging: classes.Paging):
    j = utils.select_all(
        connection=database,
        columns=["id", "autor_id", "post_id", "conteudo", "timestamp"],
        table="comentarios",
        page=paging.page,
        page_size=paging.page_size,
        where=True,
        condition_column="autor_id",
        condition_value=str(user_id)
    )
    return JSONResponse(content=j, headers=headers)


@app.get("/usuarios/{user_id}/mensagens")
async def get_user_messages(user_id: int, paging: classes.Paging):
    #j = utils.select_where(database, str(user_id), "autor_id", "mensagens", ["id", "autor_id", "mensagem", "timestamp"])
    
    j = utils.select_all(
        connection=database,
        columns=["id", "autor_id", "mensagem", "timestamp"],
        table="mensagens",
        page=paging.page,
        page_size=paging.page_size,
        where=True,
        condition_column="autor_id",
        condition_value=str(user_id)
    )

    return JSONResponse(content=j, headers=headers)


# Edição de perfil e afins

@app.post("/usuarios/{user_id}/editar/avatar")
async def edit_avatar(user_id: int, file: UploadFile, current_user_apelido: str = fastapi.Depends(auth.get_current_user)):

    file_tp = file.content_type.split("/")[1]

    # Baixar avatar do body do request
    if file_tp not in supported_image_types:
        raise fastapi.HTTPException(status_code=400, detail="Arquivo nao e uma imagem")
    
    avatar_filename = os.path.join(avatar_folder, str(user_id) + "." + file_tp)

    with open(avatar_filename, "wb+") as f:
        f.write(file.file.read())

    avatar_filename_wo_path = avatar_filename.split("/")[-1]

    utils.get_user_id(database, current_user_apelido)
    utils.update_data(database, "usuarios", "avatar_filename", "id", str(user_id), avatar_filename_wo_path)    

    
    j = {"avatar_filename": avatar_filename_wo_path}
    return JSONResponse(content=j, headers=headers)


@app.post("/usuarios/{user_id}/editar/biografia")
async def edit_bio(bio: classes.Bio, user_id: int, current_user_apelido: str = fastapi.Depends(auth.get_current_user)):
    utils.get_user_id(database, current_user_apelido)

    utils.update_data(database, "usuarios", "biografia", "id", str(user_id), str(bio.texto))    

    j = {"status": "OK"}
    return JSONResponse(content=j, headers=headers)


@app.post("/usuarios/{user_id}/editar/assinatura")
async def edit_signature(signature: classes.Signature, user_id: int, current_user_apelido: str = fastapi.Depends(auth.get_current_user)):
    utils.get_user_id(database, current_user_apelido)

    utils.update_data(database, "usuarios", "assinatura", "id", str(user_id), str(signature.assinatura))    

    j = {"status": "OK"}
    return JSONResponse(content=j, headers=headers)


# Deleção de coisas
@app.post("/usuarios/{user_id}/deletar")
async def delete_user(user_id: int, current_user_apelido: str = fastapi.Depends(auth.get_current_user)):
    utils.get_user_id(database, current_user_apelido)

    proccess = [utils.update_data(database, "usuarios", "apelido", "id", str(user_id), deletion),
                utils.update_data(database, "usuarios", "hash_senha", "id", str(user_id), deletion),
                utils.update_data(database, "usuarios", "avatar_filename", "id", str(user_id),deletion),
                utils.update_data(database, "usuarios", "biografia", "id", str(user_id), deletion),
                utils.update_data(database, "usuarios", "deletado", "id", str(user_id), "true")]

    delete = True
    for p in proccess:
        if not p:
            delete = False
            break

    if not delete:
        raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    
    j = {"status": "Bye :("}

    return JSONResponse(content=j, headers=headers)


@app.post("/posts/{post_id}/deletar")
async def delete_post(post_id: int, current_user_apelido: str = fastapi.Depends(auth.get_current_user)):
    user_id = utils.get_user_id(database, current_user_apelido)

    utils.check_existence(database, "posts", "id", str(post_id))
    
    post_data = utils.select_where(database, str(post_id), "id", "posts", ["id", "autor_id", "titulo", "conteudo", "timestamp"])

    post = post_data["posts"][0]

    if post["autor_id"] != user_id:
        raise fastapi.HTTPException(status_code=401, detail="Nao autorizado")
    
    proccess = [
        utils.update_data(database, "posts", "titulo", "id", str(post_id), deletion),
        utils.update_data(database, "posts", "conteudo", "id", str(post_id), deletion),
        utils.update_data(database, "posts", "deletado", "id", str(post_id), "true"),
    ]

    if False in proccess:
        raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    
    j = {"status": "OK"}

    return JSONResponse(content=j, headers=headers)


@app.post("/comentarios/{comment_id}/deletar")
async def delete_comment(comment_id: int, current_user_apelido: str = fastapi.Depends(auth.get_current_user)):
    user_id = utils.get_user_id(database, current_user_apelido)

    utils.check_existence(database, "comentarios", "id", str(comment_id))
    
    comment_data = utils.select_where(database, str(comment_id), "id", "comentarios", ["id", "autor_id", "post_id", "conteudo", "timestamp"])

    comment = comment_data["comentarios"][0]

    if comment["autor_id"] != user_id:
        raise fastapi.HTTPException(status_code=401, detail="Nao autorizado")
    
    proccess = [
        utils.update_data(database, "comentarios", "conteudo", "id", str(comment_id), deletion),
        utils.update_data(database, "comentarios", "deletado", "id", str(comment_id), "true"),
    ]

    if False in proccess:
        raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    
    j = {"status": "OK"}
    return JSONResponse(content=j, headers=headers)


@app.post("/mensagens/{message_id}/deletar")
async def delete_message(message_id: int, current_user_apelido: str = fastapi.Depends(auth.get_current_user)):
    logged_id = utils.get_user_id(database, current_user_apelido)

    utils.check_existence(database, "mensagens", "id", str(message_id))
    
    message_data = utils.select_where(database, str(message_id), "id", "mensagens", ["id", "autor_id", "mensagem", "timestamp"])

    message = message_data["mensagens"][0]

    if message["autor_id"] != logged_id:
        raise fastapi.HTTPException(status_code=401, detail="Acesso negado")
    
    proccess = [
        utils.update_data(database, "mensagens", "mensagem", "id", str(message_id), deletion),
        utils.update_data(database, "mensagens", "deletado", "id", str(message_id), "true"),
    ]

    if False in proccess:
        raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    
    j = {"status": "OK"}
    return JSONResponse(content=j, headers=headers)


# Search

@app.get("/pesquisar/posts/{search_term}")
async def search_posts(search_term: str, pagging: classes.Paging):
    result = utils.search(database, ["id", "autor_id", "titulo", "conteudo", "timestamp"], "posts", search_term, "titulo", pagging.page, pagging.page_size)
    
    for post in result["posts"]:
        post["comentarios"] = []
        post["autor"] = utils.select_where(database, post["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]
        comentarios = utils.select_where(database, post["id"], "post_id", "comentarios", ["id", "autor_id", "post_id", "conteudo", "timestamp"])
        
        if comentarios:
            for comentario in comentarios["comentarios"]:
                comentario["autor"] = utils.select_where(database, comentario["autor_id"], "id", "usuarios", ["apelido"])["usuarios"][0]["apelido"]
                post["comentarios"].append(comentario)

    return JSONResponse(content=result, headers=headers)


@app.get("/pesquisar/usuarios/{search_term}")
async def search_users(search_term: str, pagging: classes.Paging):
    result = utils.search(database, ["id", "apelido", "avatar_filename"], "usuarios", search_term, "apelido", pagging.page, pagging.page_size)

    return JSONResponse(content=result, headers=headers)


# Conseguir artquivos de mídia

@app.get("/arquivos/avatares/{filename}")
async def get_media(filename: str):
    return FileResponse(f"{avatar_folder}/{filename}")

@app.get("/arquivos/mural/{filename}")
async def get_media(filename: str):
    return FileResponse(f"{media_folder}/{filename}")
