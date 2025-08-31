import pydantic

class UserCreate(pydantic.BaseModel):
    apelido: str
    link_avatar: pydantic.HttpUrl
    senha: str


class Publish(pydantic.BaseModel):
    autor_id: int
    autor_apelido: str
    senha: str
    titulo: str
    conteudo: str


class Comment(pydantic.BaseModel):
    autor_id: int
    autor_apelido: str
    senha: str
    post_id: int
    conteudo: str


class SendMessage(pydantic.BaseModel):
    autor_id: int
    autor_apelido: str
    senha: str
    mensagem: str
    
