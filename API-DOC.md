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

Preencha o arquivo config.json com as configurações feitas na hora da instalação. Por padrão, as configurações são assim:
```json
{
    "database": {
        "name": "public",
        "host": "127.0.0.1",
        "port": 5432
    },
    "app": {
        "text_on_deletion": "Excluído"
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

# 3.1 Preparações

Caso tenha acabado de instalar, crie um usuário para poder testar a api caso sinta que precise.

Para isso, basta fazer um POST para ```127.0.0.1:9090/usuarios```. Coloque em ```body``` algo nesse modelo:

```json
{
	"apelido": "nickname",
	"link_avatar": "https://urlvatar.com/foto-perfil.png",
	"senha": "senhamuitoforte"
}
```

# 3.2 Conseguir token de autenticação

Para conseguir o token de autenticação, basta fazer um POST para ```127.0.0.1:9090/token```. Coloque em ```body``` algo como abaixo, além de definir ```Content-Type``` como ```application/x-www-form-urlencoded```.

```
username=nickname&password=senhamuitoforte
```

Substitua ```nickname``` e ```senhamuitoforte``` pelos seus respectivos valores.

O resultado será algo parecido como ```Bearer eyC4rr4ct3r3sT0ken```. Coloque o valor que se parece com isso no cabeçalho ```Authorization``` em todo request POST. Os passos seguintes será assumido que esse header estará presente.