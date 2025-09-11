import pydantic

class UserCreate(pydantic.BaseModel):
    apelido: str
    senha: str


class Publish(pydantic.BaseModel):
    titulo: str
    conteudo: str
    categoria_id: int


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


class PagingPosts(Paging):
    categoria_id: int


class Signature(pydantic.BaseModel):
    assinatura: str


class Category(pydantic.BaseModel):
    titulo: str
    desc: str


class ResourceInfo(pydantic.BaseModel):
    resource_type: str
    resource_id: int


class ResourcePaging(ResourceInfo):
    page: int
    page_size: int
