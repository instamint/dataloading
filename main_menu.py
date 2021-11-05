import time, InstamintLoaderBlue, InstamintLoaderRed, InstamintLoaderDefault
import pandas as pd
import csv
from datetime import datetime

date = datetime.now()

menu = ['usr','roles','erc721Contract','token','erc721token','portfolio','trade','truncate_all']

menu_db = ['Default','Blue', "Red"]

def display_menu():
    try:
        for item_db_menu in menu_db:
            print(menu_db.index(item_db_menu)+1,': ', item_db_menu)        
        choice_db = int(input('Select DataBase: '))
        choice_db_str = menu_db[choice_db - 1]

        for m in menu:
            print(menu.index(m)+1,': ',m)
        choice = int(input('Select Table: '))       
        choice_str = menu[choice - 1]

        res_str = choice_db_str +"|"+ choice_str
    except:
        res_str = "Error, invalid option"
        print(res_str)

    return res_str


opt = display_menu()

if opt[0] == "Red":
    il = InstamintLoaderRed.InstamintLoader()
elif opt[0] == "Blue":
    il = InstamintLoaderBlue.InstamintLoader()
elif opt[0] == "Default":
    il = InstamintLoaderDefault.InstamintLoader()


if opt == "usr":
    il.add_usr(username='adminuser',name='Admin User',email_domain='instamint.com', n_rows =20, bulk=1, role_id=2)
elif opt == 'roles':
    il.add_roles()

elif opt == "erc721Contract":
    il.add_erc721Contract(n_rows=100)

elif opt == "token":
    il.add_token(n_rows=100)

#this part is going to change so every field of the csv are part of a list
elif opt == "erc721token":
  
    with open('erc721tokens.csv') as f:
        data=[tuple(line) for line in csv.reader(f)]

    n_token = 1
    n_contract = 1
    for row in data:
        
        item = row[0].split(',')
        if item[0] != "ID":
            arr_item = ''

            id = item[0]
            
            instagram_username   = item[1]
            instagram_pic_share  = item[2]
            instagram_direct_url = item[3]
            
            wasabi_url     = item[4]
            vintage_date   = item[5]
            image_ipfs_cid = item[6]
            image_ipfs_url = item[7]
            metadata_cid   = item[8]
            
            metadata_ipfs_url = item[9]
            _contract_address  = item[10]

            token_id = item[11]

            _metadata = "{userid="+ id +", source=instagram, instaId=18136185625236950, instaUserName='"+ instagram_username +"', instaUrl='"+ instagram_direct_url + \
                       "', localStoreUrl='"+ wasabi_url +"', mintTimeStamp='"+ str(datetime.now()) +"', name='"+instagram_username+ \
                       "', title='TEST', description='test', totalSupply='', secretHash='2bac7f27bb709bf1b1c6119db18079f0ba63169c3cd95fb7fc3ae0348cb890f8'}"
            
            il.add_erc721token(createdby=4,description="test mint nft desciption", n_rows=1, ipfs_image_cid=image_ipfs_cid, image_ipfs_url=image_ipfs_url, name="test mint ntf", \
                                meta_data=_metadata, image_web_url=wasabi_url, contract_id=n_contract,token_id=n_token, meta_data_ipfs_cid=metadata_cid, meta_data_ipfs_url=metadata_ipfs_url)

            n_token+=1
            n_contract+=1

elif opt =="portfolio":
    il.add_portfolio(n_rows=1)

elif opt == "trade":
    il.add_trades(n_rows=100)

elif opt == "truncate_all":
    il.truncate_all()      

 

 