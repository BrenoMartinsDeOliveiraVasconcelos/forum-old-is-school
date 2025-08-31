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

