import logging
import pyodbc

from model.common import *

table_name = 'PengumumanOJK_file'


def save_bulk_file(bulk_insert):
    columns = ', '.join(bulk_insert[0].keys())
    placeholders = ', '.join('?' for _ in bulk_insert[0].keys())
    formatted_items = ', '.join(f"({placeholders})" for _ in bulk_insert)

    sql = (f"INSERT INTO {table_name} ({columns}) VALUES {formatted_items};")
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        values = create_value(bulk_insert)
        result = cursor.execute(sql, values)
        conn.commit()
        return result

    except pyodbc.Error as e:
        logging.error(f"Error inserting/updating data: {e}")
        return []

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()


def create_value(data):
    return [item for sublist in data for item in sublist.values()]
