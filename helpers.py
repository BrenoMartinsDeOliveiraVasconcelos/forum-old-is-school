import utils
import psycopg2


def get_user_data(database: psycopg2.extensions.connection, user_id: str):
    return  utils.select_where(database, user_id, "id", "usuarios", ["id", "apelido", "avatar_filename"])["usuarios"][0]