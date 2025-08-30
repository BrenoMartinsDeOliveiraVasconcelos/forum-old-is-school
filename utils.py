import hashlib
import re
import psycopg2

REGEXES = {
    "url": "https?:\/\/(?:www\.)?([-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b)*(\/[\/\d\w\.-]*)*(?:[\?])*(.+)*",
    "username": "^([A-Z]|[a-z]|[0-9]|-|_){1,}$"
}

def validate(data, type):
    if type == "url":
        return re.match(REGEXES["url"], data)
    elif type == "username":
        return re.match(REGEXES["username"], data)


def generate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()


def get_connection(db_config: dict, postgree_user: str, postgree_password: str):
    return psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        database=db_config["name"],
        user=postgree_user,
        password=postgree_password
    )


def query(connection: psycopg2.extensions.connection, query: str, query_params: tuple):
    cursor = connection.cursor()
    cursor.execute(query, query_params)
    connection.commit()

    last_row_added = cursor.fetchone()
    cursor.close()

    return last_row_added