# forum-old-is-school

# 1 - Requisitos minimos

| Item | Valor |
| --- | --- |
| SO | Windows 10 ou superior; Limux |
| Programas | PostgresSQL, Python 3.10+ |
| Bibliotecas | Ver requirements.txt |
| RAM | 2 GB ou mais |
| Armazenamento | Depende do uso |
| Processador | 2 Ghz ou mais |

# 2 - Configuração

## 2.1 Instalar e configurar PostgresSQL

### 2.1.1 Windows

Instale o PostgresSQL com locale UTF-8 ou pt-br.UTF8.

[Ver instuções no W3Schools](https://www.w3schools.com/postgresql/postgresql_install.php)

### 2.1.2 Linux

Instale o pacote do PostgresSQL.

**Debian/Ubuntu e derivados**

```bash
sudo apt-get install postgresql postgresql-contrib
```

Verificar sua distribuição para outros sistemas.

Após isso, deve configurar uma senha para o usuário postgres caso vá usar ele.

Entre no shell

```bash
sudo -u postgres psql
```

Troque a senha
```
 \password postgres
```

## 2.2 Configurar banco de dados

Nesse documento, usamos o usuário padrão e banco de dados padrão ```postgres```. Sinta-se livre para criar outro caso tenha mais experiência.

Execute as instruções no arquivo db.sql no usuário especificado no banco ```public``` que vem por padrão. Ou, configure o própio banco caso se sinta confortável e execute as instruções.

## 2.3 Configurar o arquivo config.json

Preencha o arquivo config.json com as configurações feitas na hora da instalação. Aqui está um exemplo de um JSON funcional com base nas configuraçõe padrão.
```json
{
    "database": {
        "name": "postgres",
        "host": "127.0.0.1",
        "port": 5432
    },
    "app": {
        "text_on_deletion": "Excluído",
        "data_path": "./data"
    }
}
```

## 2.4 Criar variáveis de ambiente

No seu sistema, crie as seguintes variáveis de ambiente:

```python
P_USER = "postgres" # Ou outro usuário, caso tenha configurado outro
P_PASSWORD = "senha" # Substua pela senha do usuário
SECRET_KEY = "chavesupersecreta" # Gere uma chave com 'openssl rand -hex 32'
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Ou qualquer outro numero de sua preferencia
```

Reinicie o computador.

## 2.5 Instalar bibliotecas Python

Após ter instalado Python no seu sistema, execute os comandos abaixo no diretório onde está os arquivos da api.

OBS: É recomendado usar em um ambiente virtual.

```bash
pip install -r requirements.txt
uvicorn app:app --port 9090 --host 127.0.0.1
```

Sendo ```--port``` a porta que a api vai responder e ```--host``` o ip.

# 3 - Usando a API

Durante a documentação, será usado 127.0.0.1 como ip e 9090 como porta parta fins de facilitar. Caso tenha uma outra configuração, substitua. Valhe ressaltar que, exceto quando dito explicitamente, sempre deve ser colocado um header ```Content-Type``` como ```application/json```.

## 3.1 Preparações

Caso tenha acabado de instalar, crie um usuário para poder testar a api caso sinta que precise.

Para isso, basta fazer um POST para ```127.0.0.1:9090/usuarios```. Coloque em ```body``` algo nesse modelo:

```json
{
	"apelido": "nickname",
	"senha": "senhamuitoforte"
}
```

## 3.2 Conseguir token de autenticação

Para conseguir o token de autenticação, basta fazer um POST para ```127.0.0.1:9090/token```. Coloque em ```body``` algo como abaixo, além de definir ```Content-Type``` como ```application/x-www-form-urlencoded```.

```
username=nickname&password=senhamuitoforte
```

Substitua ```nickname``` e ```senhamuitoforte``` pelos seus respectivos valores.

O resultado será algo parecido como ```Bearer eyC4rr4ct3r3sT0ken```. Coloque o valor que se parece com isso no cabeçalho ```Authorization``` em todo request POST. Os passos seguintes será assumido que esse header estará presente.'

## 3.3 Endopoins

**Nota: Em regra, todos os ```body``` são em JSON e cada key é uma string exceto caso dito explicitamente o contrário.**

### 3.3.1 /usuarios

Esse endpoint é relacionado manipulação e obteção de dados de usuários. 

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| GET | - | ```page: int```, ```page_size: int``` | Lista de usuários | - |
| POST | - | ```apelido```, ```senha``` | ```user_id``` | - |

#### 3.3.1.1 /usuarios/user_id

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| GET | ```user_id``` | ```page: int```, ```page_size: int``` | Lista com o usuário e todos os seus posts, comentários e mensagens | - |

##### 3.3.1.1.1 /usuarios/user_id/posts

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| GET | ```user_id``` | ```page: int```, ```page_size: int``` | | Lista de posts feito pelo usuário | - |

##### 3.3.1.1.2 /usuarios/user_id/comentarios

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| GET | ```user_id``` | ```page: int```, ```page_size: int``` | | Lista de comentários feito pelo usuário | - |

##### 3.3.1.1.3 /usuarios/user_id/mensagens

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| GET | ```user_id``` | ```page: int```, ```page_size: int``` | | Lista de mensagens enviadas pelo usuário | - |

#### 3.3.1.2 /usuarios/user_id/editar

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| - | - | - | - | Raiz de edição |

##### 3.3.1.2.1 /usuarios/user_id/editar/avatar


| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| POST | ```user_id``` | ```file``` |Um status OK junto ao nome do arquivo | Body tem Content-Type multipart/form-data |

##### 3.3.1.2.2 /usuarios/user_id/editar/biografia

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| POST | ```user_id``` | ```biografia``` | ```status: ok```| - |

##### 3.3.1.2.2 /usuarios/user_id/editar/assinatura

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| POST | ```user_id``` | ```assinatura``` | ```status: ok```| - |


#### 3.3.1.3 /usuarios/user_id/deletar

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| POST | ```user_id``` | - | ```status: bye :(```| - |
 
### 3.3.2 /posts

Endpoint relacionado a posts. Possui uma quanitdade menor de chamdas em relação a /usuarios

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| GET | - | ```page: int```, ```page_size: int``` | Lista de posts | - |
| POST | - | ```titulo```, ```conteudo``` | ```status: ok```| - |


#### 3.3.2.1 /posts/post_id

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| GET | ```post_id``` | - | Lista com o post e todos os seus comentários | - |


##### 3.3.2.1.1 /posts/post_id/deletar

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| POST | ```post_id``` | - | ```status: ok```| - |


### 3.3.3 /mural

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| POST | - | ```file: arquivo```, ```titulo```, ```conteudo``` |Um status OK junto ao nome do arquivo | Body tem Content-Type multipart/form-data |

### 3.3.4 /comentarios

Endpoint de comentários.

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| GET | - | ```page: int```, ```page_size: int``` | Lista de comentários | - |
| POST | - | ```post_id```, ```conteudo``` | ```status: ok```| - |


#### 3.3.4.1 /comentarios/comentario_id

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| GET | ```comentario_id``` | - | Lista com o comentário | - |


##### 3.3.4.1.1 /comentarios/comentario_id/deletar

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| POST | ```comentario_id``` | - | ```status: ok```| - |

### 3.3.5 /mensagens

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| GET | - | ```page: int```, ```page_size: int``` | Lista de mensagens | - |
| POST | - | ```mensagem``` | ```status: ok```| - |


#### 3.3.5.1 /mensagens/mensagem_id

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| GET | ```mensagem_id``` | - | Lista com a mensagem | - |  


##### 3.3.5.1.1 /mensagens/mensagem_id/deletar

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| POST | ```mensagem_id``` | - | ```status: ok```| - |

### 3.3.6 /pesquisar

Esse endpoint não é aceito na raiz

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| - | - | - |- | - |

#### 3.3.6.1 /pesquisar/posts/search_term

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| GET | ```search_term``` | ```page: int```, ```page_size: int``` | Lista de posts correspondente a pesquisa | - |

#### 3.3.6.2 /pesquisar/usuarios/search_term

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| GET | ```search_term``` | ```page: int```, ```page_size: int``` | Lista de usuarios correspondente a pesquisa | - |


### 3.3.7 /arquivos

Esse endpoint é responsável por pegar arquivos de mídia do servidor. Só recebe métodos GET

#### 3.3.7.1 /arquivos/avatares/arquivo

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| GET | ```arquivo``` | - | O arquivo em questão | - |

#### 3.3.7.2 /arquivos/mural/arquivo

| Requests suportados | Argumentos na URL | Body | Retorno | OBS |
| --- | --- | --- | --- | --- |
| GET | ```arquivo``` | - | O arquivo em questão | - |


# 4 - Status codes

A API possui um sistema consistente de status code, retornando um códiggo HTTP de erro caso algo esteja errado.

| Códigos | Descrição |
| --- | --- |
| 400 | O request possui um erro |
| 401 | Acesso negado ao recurso |
| 404 | Recurso não encontrado |
| 409 | O request poussui um valor que deve ser unico, mas esse valor já existe |
| 500 | Erro no servidor |
