import config, time, sql
from datetime import datetime
import psycopg, os, random
from dotenv import load_dotenv
class InstamintLoader():
    def __init__(self):
        self.conn = self.get_conn()
        self.cur = self.conn.cursor()
    def add_chain(self,chain):
        self.cur.execute('INSERT INTO CHAIN (created_by,created_dt,last_modified_by,updated_dt,name) VALUES (%s,%s,%s,%s,%s)', 
        (1,datetime.now(),1,datetime.now(),chain))

    def add_usr(self,username,name,email_domain,profile_url=None,password='$2a$10$e7Wvy/dj49K9r4JaLmt/TuTkEtLvE9MGP3Eh7aJ0bLxB4acxxHE2K',disabled=False,bulk=1,start_bulk=0):
        if profile_url == None:
            profile_url = random.choice(InstamintLoader.profile_urls)
        if bulk==1:
            self.cur.execute('INSERT INTO USR (EMAIL,USER_NAME,FULL_NAME,IS_DISABLED,PASSWORD,PROFILE_PHOTO_URL,CREATED_BY,CREATED_DT) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', 
            (username + '@' + email_domain,username,name,disabled,password,profile_url,1,datetime.now()))
        else:
            for n in range(start_bulk,start_bulk+bulk+1):
                self.cur.execute('INSERT INTO USR (EMAIL,USER_NAME,FULL_NAME,IS_DISABLED,PASSWORD,PROFILE_PHOTO_URL,CREATED_BY,CREATED_DT) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(username+str(n)+ '@' + email_domain,username+str(n),name+str(n),disabled,password,random.choice(InstamintLoader.profile_urls),1,datetime.now()))

    def commit(self):
        self.conn.commit()
    def get_conn(self):
        load_dotenv(".env")
        dbname = os.environ.get('instamint_db_dbname')
        user = os.environ.get('instamint_db_user')
        pwd = os.environ.get('instamint_db_password')
        host = os.environ.get('instamint_db_host')
        port = os.environ.get('instamint_db_port')
        conn = psycopg.connect(dbname=dbname, user=user, password=pwd, host=host,port=port)
        return conn
    profile_urls = [
    'https://preview.keenthemes.com/metronic8/demo3/assets/media/avatars/150-11.jpg',
    'https://preview.keenthemes.com/metronic8/demo3/assets/media/avatars/150-3.jpg',
    'https://preview.keenthemes.com/metronic8/demo3/assets/media/avatars/150-4.jpg',
    'https://preview.keenthemes.com/metronic8/demo3/assets/media/avatars/150-5.jpg',
    'https://preview.keenthemes.com/metronic8/demo3/assets/media/avatars/150-6.jpg'
    ]


