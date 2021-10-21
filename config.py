import psycopg, os
from dotenv import load_dotenv
def get_conn():
    load_dotenv(".env")
    dbname = os.environ.get('instamint_db_dbname')
    user = os.environ.get('instamint_db_user')
    pwd = os.environ.get('instamint_db_password')
    host = os.environ.get('instamint_db_host')
    port = os.environ.get('instamint_db_port')
    conn = psycopg.connect(dbname=dbname, user=user, password=pwd, host=host,port=port)
    return conn