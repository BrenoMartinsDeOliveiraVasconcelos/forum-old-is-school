import utils
import psycopg2


def get_user_data(database: psycopg2.extensions.connection, user_id: str):
    return  utils.select_where(database, user_id, "id", "usuarios", ["id", "apelido", "avatar_filename"])["usuarios"][0]

def update_multiple_data(database: psycopg2.extensions.connection, table: str, columns: list, condition_column: str, condition_value: str, new_values: list):
    for i in range(len(columns)):
        utils.update_data(database, table, columns[i], condition_column, condition_value, new_values[i])
    
