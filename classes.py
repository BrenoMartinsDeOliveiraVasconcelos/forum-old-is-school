import pydantic

class UserCreate(pydantic.BaseModel):
    apelido: str
    link_avatar: pydantic.HttpUrl
    senha: str


class Publish(pydantic.BaseModel):
    titulo: str
    conteudo: str


class Comment(pydantic.BaseModel):
    post_id: int
    conteudo: str


class SendMessage(pydantic.BaseModel):
    mensagem: str


class Avatar(pydantic.BaseModel):
    link_avatar: pydantic.HttpUrl


class Bio(pydantic.BaseModel):
    texto: str


class Paging(pydantic.BaseModel):
    page: int
    page_size: int
