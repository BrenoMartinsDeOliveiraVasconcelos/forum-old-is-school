import utils
import psycopg2
import classes
import fastapi
from fastapi.responses import JSONResponse

COMMON_HEADERS = {"Access-Control-Allow-Origin": "*"}

def get_user_data(database: psycopg2.extensions.connection, user_id: str):
    return  utils.select_where(database, user_id, "id", "usuarios", ["id", "apelido", "avatar_filename", "admin"])["usuarios"][0]

def update_multiple_data(database: psycopg2.extensions.connection, table: str, columns: list, condition_column: str, condition_value: str, new_values: list):
    for i in range(len(columns)):
        utils.update_data(database, table, columns[i], condition_column, condition_value, new_values[i])
    

def get_boolean_status(database: psycopg2.extensions.connection, resource_info: classes.ResourceInfo, boolean_column: str):
    return utils.select_where(database, str(resource_info.resource_id), "id", resource_info.resource_type, [boolean_column], ignore_deleted=False)[resource_info.resource_type][0][boolean_column]


def append_signature(database: psycopg2.extensions.connection, user_id: str, content: str):
    user_sign = utils.select_where(database, user_id, "id", "usuarios", ["assinatura"])["usuarios"][0]["assinatura"]

    if user_sign:
        content += "\n\n" + user_sign

    return content


def soft_delete_resource_owner(
    db_connection, 
    resource_type: str, 
    resource_id: int, 
    user_id: int, 
    fields_to_clear: list[str],
    deletion_text: str
):
    utils.check_existence(db_connection, resource_type, "id", str(resource_id))
    
    resource_data = utils.select_where(db_connection, str(resource_id), "id", resource_type, ["autor_id"])
    resource_owner_id = resource_data[resource_type][0]["autor_id"]

    if resource_owner_id != user_id:
        raise fastapi.HTTPException(status_code=401, detail="Nao autorizado")
    
    update_fields = fields_to_clear + ["deletado", "deletor_id"]
    update_values = [deletion_text] * len(fields_to_clear) + ["true", str(user_id)]
    
    update_multiple_data(db_connection, resource_type, update_fields, "id", str(resource_id), update_values)


def insert_user_data(db_connection, items: list[dict], author_id_key: str = "autor_id"):
    for item in items:
        if author_id_key in item:
            item["autor"] = get_user_data(db_connection, item[author_id_key])
    return items


def api_response(content: dict, status_code: int = 200):
    return JSONResponse(content=content, status_code=status_code, headers=COMMON_HEADERS)
