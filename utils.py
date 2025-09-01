import hashlib
import re
import psycopg2
from psycopg2 import sql
import traceback

REGEXES = {
    "url": "https?:\/\/(?:www\.)?([-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b)*(\/[\/\d\w\.-]*)*(?:[\?])*(.+)*",
    "username": "^([A-Z]|[a-z]|[0-9]|-|_){1,}$"
}

ERROR_CODES = {
    "TOO_LONG": 1
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


def authenticate(connection: psycopg2.extensions.connection, username: str, password: str):
    result = query(connection, "SELECT * FROM usuarios WHERE apelido = %s AND hash_senha = %s;", (username, generate_hash(password)))

    if result is not None:
        return True
    else:
        return False
    

def query(connection: psycopg2.extensions.connection, query: str, query_params: tuple) -> tuple | None | bool | int:
    cursor = connection.cursor()
    cursor.execute(query, query_params)

    last_row_added = cursor.fetchone()

    return last_row_added


def select_all(connection: psycopg2.extensions.connection, columnns: list, table: str) -> dict:
    cursor = connection.cursor()
    cursor.execute(f"SELECT {', '.join(columnns)} FROM {table};")
    rows = cursor.fetchall()

    result = {f"{table}": []}

    for row in rows:
        result[f"{table}"].append(dict(zip(columnns, row)))

    return result



def get_user_id(connection: psycopg2.extensions.connection, username: str):
    result = select_where(connection, username, "apelido", "usuarios", ["id"])

    if result is not None:
        return result["usuarios"][0]["id"]
    else:
        return False
    

def select_where(connection: psycopg2.extensions.connection, value: str, comun_fetch: str, table_fetch: str, return_columns: list) -> dict:
    cursor = connection.cursor()
    
    query_sql = sql.SQL("SELECT {columns} FROM {table} WHERE {condition_column} = %s").format(
        columns=sql.SQL(', ').join(map(sql.Identifier, return_columns)),
        table=sql.Identifier(table_fetch),
        condition_column=sql.Identifier(comun_fetch)
    )

    cursor.execute(query_sql, (value,))
    rows = cursor.fetchall()

    result = {f"{table_fetch}": []}

    if not rows:
        return {}
    for row in rows:
        result[f"{table_fetch}"].append(dict(zip(return_columns, row)))

    return result


def insert_into(connection: psycopg2.extensions.connection, table: str, columns: list, values: list, returning: str):
    cursor = connection.cursor()

    query_sql = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING {returning};").format(
        table=sql.Identifier(table), 
        columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
        values=sql.SQL(', ').join(map(sql.Literal, values)),
        returning=sql.Identifier(returning))

    try:
        cursor.execute(query_sql)
        connection.commit()
        result = cursor.fetchone()

        return result
    except (psycopg2.errors.UniqueViolation):
        item_return = False
    except (psycopg2.errors.StringDataRightTruncation):
        item_return = ERROR_CODES["TOO_LONG"]

    connection.rollback()

    return item_return


def check_existence(connection: psycopg2.extensions.connection, table: str, column: str, value: str):
    result = select_where(connection, value, column, table, ["id"])

    if not result:
        return False
    else:
        return True
    

def update_data(connection: psycopg2.extensions.connection, table: str, column: str, condition_column: str, condition_value: str, new_value: str):
    cursor = connection.cursor()

    try:
        query_sql = sql.SQL("UPDATE {table} SET {column} = %s WHERE {condition_column} = %s;").format(
            table=sql.Identifier(table), 
            column=sql.Identifier(column),
            condition_column=sql.Identifier(condition_column))

        cursor.execute(query_sql, (new_value, condition_value))
        connection.commit()

        return True
    except Exception as e:
        print(traceback.format_exc())

    connection.rollback()
    return False

