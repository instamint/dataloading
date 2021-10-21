import config, time, sql
from datetime import datetime
date = datetime.now() #time.time() #datetime.date(2020, 11, 18)
conn = config.get_conn()
cur = conn.cursor()
il = sql.InstamintLoader()

# Add users
# for n in range(10,21):
#     il.add_usr('johnuser'+str(n),'John Smith'+str(n),'john'+str(n)+'@emailsys.com')

il.add_usr(username='jamiel',name='Jamiel Sheikh',email_domain='instamint.com')


#il.add_usr(username='baduser',name='Bad Smith',email_domain='proton.com',bulk=5,start_bulk=5,disabled=True)

# il.add_chain('polygon')
# il.add_chain('immutable')
# il.add_chain('avalanche')
il.commit()



# with conn.cursor() as cur:
#     cur.execute('select * from erc721_contract')
#     for r in cur:
#         print(r)
#     cur.execute('select * from ask_history')
#     for r in cur:
#         print(r)
#     cur.execute('INSERT INTO USR (EMAIL,USER_NAME,FULL_NAME,IS_DISABLED,PASSWORD,PROFILE_PHOTO_URL,CREATED_BY,CREATED_DT) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', 
#     ('test4@test4.com','testname4','Full Name4',False,'password','some url',1,date))


