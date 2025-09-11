import utils
import psycopg2
import classes


def get_user_data(database: psycopg2.extensions.connection, user_id: str):
    return  utils.select_where(database, user_id, "id", "usuarios", ["id", "apelido", "avatar_filename", "admin"])["usuarios"][0]

def update_multiple_data(database: psycopg2.extensions.connection, table: str, columns: list, condition_column: str, condition_value: str, new_values: list):
    for i in range(len(columns)):
        utils.update_data(database, table, columns[i], condition_column, condition_value, new_values[i])
    

def get_boolean_status(database: psycopg2.extensions.connection, resource_info: classes.ResourceInfo, boolean_column: str):
    return utils.select_where(database, str(resource_info.resource_id), "id", resource_info.resource_type, [boolean_column], ignore_deleted=False)[resource_info.resource_type][0][boolean_column]
