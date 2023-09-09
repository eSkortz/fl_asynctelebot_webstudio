import sqlite3
import config

database_path = config.db_path

def first_connect_from_user():
    database = sqlite3.connect(database_path)
    cursor = database.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS requests(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, tnumber TEXT, content TEXT, 
        status TEXT);""")
    database.commit()
    database.close()


def get_requests_new():
    database = sqlite3.connect(database_path)
    cursor = database.cursor()
    cursor.execute("SELECT * FROM requests WHERE status = 'new';")
    requests_new = cursor.fetchall()
    database.close()
    return requests_new


def get_requests_in_processing():
    database = sqlite3.connect(database_path)
    cursor = database.cursor()
    cursor.execute("SELECT * FROM requests WHERE status = 'in_processing';")
    requests_in_processing = cursor.fetchall()
    database.close()
    return requests_in_processing


def get_requests_accepted():
    database = sqlite3.connect(database_path)
    cursor = database.cursor()
    cursor.execute("SELECT * FROM requests WHERE status = 'accepted';")
    requests_accepted = cursor.fetchall()
    database.close()
    return requests_accepted


def get_requests_declined():
    database = sqlite3.connect(database_path)
    cursor = database.cursor()
    cursor.execute("SELECT * FROM requests WHERE status = 'declined';")
    requests_declined = cursor.fetchall()
    database.close()
    return requests_declined


def get_request_by_id(request_id):
    database = sqlite3.connect(database_path)
    cursor = database.cursor()
    cursor.execute(f"SELECT * FROM requests WHERE id = {request_id};")
    request = cursor.fetchall()
    database.close()
    return request


def update_request_status_by_id(request_id, status):
    database = sqlite3.connect(database_path)
    cursor = database.cursor()
    cursor.execute(f'UPDATE requests SET status = "{status}" WHERE id = {request_id}')
    database.commit()
    database.close()


    