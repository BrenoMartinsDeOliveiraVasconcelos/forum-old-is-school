import hashlib
import re
import psycopg2
from psycopg2 import sql
import traceback
import fastapi
import datetime

REGEXES = {
    "url": "https?:\\/\\/(?:www\\.)?([-a-zA-Z0-9@:%._\\+~#=]{2,256}\\.[a-z]{2,6}\b)*(\\/[\\/\\d\\w\\.-]*)*(?:[\\?])*(.+)*",
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
        password=postgree_password,
        client_encoding='utf-8'
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


def select_all(
    connection: psycopg2.extensions.connection,
    columns: list,
    table: str,
    page: int = 1,
    page_size: int = 10,
    where: bool = False,
    condition_column: str = "",
    condition_value: str = "",
) -> dict:
    columns = columns.copy()
    if 'deletado' not in columns:
        columns.append('deletado')


    offset = (page - 1) * page_size

    cursor = connection.cursor()
    query = sql.SQL("""
        SELECT {columns} 
        FROM {table} 
        WHERE deletado = false {where_clause}
        ORDER BY id
        LIMIT %s OFFSET %s;
    """).format(
        columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
        table=sql.Identifier(table),
        where_clause=sql.SQL("AND {} = %s").format(sql.Identifier(condition_column)) if where else sql.SQL("")
    )

    if where:
        cursor.execute(query, (condition_value, page_size, offset))
    else:
        cursor.execute(query, (page_size, offset))
    
    
    rows = cursor.fetchall()
    result = {table: []}
    col_names = [desc[0] for desc in cursor.description]

    for row in rows:
        row_dict = {}
        for idx, col_name in enumerate(col_names):
            if col_name == 'deletado':
                continue
                
            value = row[idx]
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            row_dict[col_name] = value
        
        result[table].append(row_dict)

    result['page'] = {
        'page': page,
        'page_size': page_size,
        'has_next': len(rows) == page_size
    }
    
    return result


def select_where(connection: psycopg2.extensions.connection, value: str, comun_fetch: str, table_fetch: str, return_columns: list, raise_on_notfound: bool = False) -> dict:
    cursor = connection.cursor()
    
    return_columns.append("deletado")

    query_sql = sql.SQL("SELECT {columns} FROM {table} WHERE {condition_column} = %s").format(
        columns=sql.SQL(', ').join(map(sql.Identifier, return_columns)),
        table=sql.Identifier(table_fetch),
        condition_column=sql.Identifier(comun_fetch)
    )

    cursor.execute(query_sql, (value,))
    rows = cursor.fetchall()

    result = {f"{table_fetch}": []}

    if not rows:
        if raise_on_notfound:
            raise fastapi.HTTPException(status_code=404, detail="Item nao encontrado")
        else :
            return result
    for row in rows:
        if row[-1]:
            continue
        
        mut_row = [r for r in row]

        for i in range(len(mut_row)):
            if isinstance(mut_row[i], datetime.datetime):
                mut_row[i] = mut_row[i].strftime("%Y-%m-%d %H:%M:%S")

        result[f"{table_fetch}"].append(dict(zip(return_columns, mut_row)))

    return result


def get_user_id(connection: psycopg2.extensions.connection, username: str):
    result = select_where(connection, username, "apelido", "usuarios", ["id"])

    if result is not None:
        return result["usuarios"][0]["id"]
    else:
        raise fastapi.HTTPException(status_code=401, detail="Acesso não permitido")


def insert_into(connection: psycopg2.extensions.connection, table: str, columns: list, values: list, returning: str):
    cursor = connection.cursor()

    query_sql = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING {returning};").format(
        table=sql.Identifier(table), 
        columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
        values=sql.SQL(', ').join(map(sql.Literal, values)),
        returning=sql.Identifier(returning))
    
    rollback = True

    try:
        cursor.execute(query_sql)
        connection.commit()
        result = cursor.fetchone()
        rollback = False

        return result
    except (psycopg2.errors.UniqueViolation):
        fastapi.raise_exception(fastapi.HTTPException(status_code=409, detail="Item ja cadastrado"))
    except (psycopg2.errors.StringDataRightTruncation):
        fastapi.raise_exception(fastapi.HTTPException(status_code=400, detail="Conteudo muito longo"))
    finally:

        if rollback:
            connection.rollback()
    


def check_existence(connection: psycopg2.extensions.connection, table: str, column: str, value: str, raise_on_notfound: bool = True):
    result = select_where(connection, value, column, table, ["id"])

    if not result:
        if raise_on_notfound:
            raise fastapi.HTTPException(status_code=404, detail="Item nao encontrado")
        
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
        raise fastapi.HTTPException(status_code=500, detail="Erro interno")
    

def search(
    connection: psycopg2.extensions.connection,
    columns: list,
    table: str,
    search_term: str,
    column_search: str,    
    page: int = 1,
    page_size: int = 10
) -> dict:
    columns = columns.copy()
    if 'deletado' not in columns:
        columns.append('deletado')

    offset = (page - 1) * page_size
    query_params = [f"%{search_term}%", page_size, offset]

    query_part_1 = f"""
        SELECT {', '.join(columns)} 
        FROM {table} 
        WHERE deletado = false AND {column_search} ILIKE %s"""

    query_part_2 = """    
        ORDER BY id
        LIMIT %s OFFSET %s;
    """

    query_full = query_part_1 + query_part_2
    
    cursor = connection.cursor()
    cursor.execute(query_full, tuple(query_params))
    rows = cursor.fetchall()

    result = {table: []}
    col_names = [desc[0] for desc in cursor.description]

    for row in rows:
        row_dict = {}
        for idx, col_name in enumerate(col_names):
            if col_name == 'deletado':
                continue
                
            value = row[idx]
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            row_dict[col_name] = value
        
        result[table].append(row_dict)

    result['page'] = {
        'page': page,
        'page_size': page_size,
        'has_next': len(rows) == page_size
    }
    
    return result


def check_privileges(connection: psycopg2.extensions.connection, user_id: int):
    result = select_where(connection, user_id, "id", "usuarios", ["admin"], True)

    if not result["usuarios"][0]["admin"]:
        raise fastapi.HTTPException(status_code=401, detail="Acesso negado.")
    else:
        return True
