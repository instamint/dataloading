from math import e
import config, time, sql
from datetime import date, datetime
import psycopg, os, random
from dotenv import load_dotenv

class InstamintLoader():
    def __init__(self):
        
        self.conn = self.get_conn()
        self.cur = self.conn.cursor()

    def add_chain(self,chain):
        self.cur.execute('INSERT INTO CHAIN (created_by,created_dt,last_modified_by,updated_dt,name) VALUES (%s,%s,%s,%s,%s)', 
        (1,datetime.now(),1,datetime.now(),chain))

    def add_usr(self,username,name,email_domain,profile_url=None,password='$2a$10$e7Wvy/dj49K9r4JaLmt/TuTkEtLvE9MGP3Eh7aJ0bLxB4acxxHE2K',disabled=False,bulk=0, \
        n_rows=0, role_id=2):

        if profile_url == None:
            profile_url = random.choice(InstamintLoader.profile_urls)
        if bulk==0:
            self.cur.execute('INSERT INTO USR (EMAIL,USER_NAME,FULL_NAME,IS_DISABLED,PASSWORD,PROFILE_PHOTO_URL,CREATED_BY,CREATED_DT, ROLE_ID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)', \
            (username + '@' + email_domain,username,name,disabled,password,profile_url,1,datetime.now(), role_id))
        else:
            start_bulk=1
            n_rows +=1
            for n in range(start_bulk, n_rows):
                print(username+str(n)+ '@' + email_domain,username+str(n))
                self.cur.execute('INSERT INTO USR (EMAIL,USER_NAME,FULL_NAME,IS_DISABLED,PASSWORD,PROFILE_PHOTO_URL,CREATED_BY,CREATED_DT, ROLE_ID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)', \
                (username+str(n)+ '@' + email_domain,username+str(n),name+str(n),disabled,password,random.choice(InstamintLoader.profile_urls),1,datetime.now(), role_id))

    
    def add_erc721Contract (self, createdby=102,contract_address='0x6FCA0F70BcC4a86786c79414F8E84BD542F7c250', creator_address='dummy data', deploy_gas_fee=0, \
                            etherscan_url='https://etherscan.io/address/0x6FCA0F70BcC4a86786c79414F8E84BD542F7c250', owner_address='0x5F1d4F3F283A81Eb118FE59E2F4450C90F0e017', \
                            deploy_success=True, name='dummy data', symbol='dummy data', bulk=0, n_rows=1):

            start_bulk = 1
            
            itera = 1
            for n in range(start_bulk, n_rows + 1):
                self.cur.execute("INSERT INTO ERC721_CONTRACT (CREATED_BY, CREATED_DT, LAST_MODIFIED_BY, UPDATED_DT, CONTRACT_ADDRESS, CREATOR_ADDRESS, DEPLOY_GAS_FEE, ETHERSCAN_URL, OWNER_ADDRESS, DEPLOY_DT, " \
                                                        "DEPLOY_SUCCESS, NAME, SYMBOL) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ", \
                            (createdby,datetime.now(), createdby ,datetime.now(), contract_address, creator_address, deploy_gas_fee, etherscan_url, owner_address, datetime.now(), deploy_success, name + " " + \
                            str(itera), symbol + " " + str(itera)))
                itera+=1

    
    def add_erc721token (self, bulk=0, createdby=102, description='test description', n_rows=1, ipfs_image_cid='dummy data', image_ipfs_url='dummy data', meta_data = 'dummy data', \
                         meta_data_ipfs_cid ='dummy data', meta_data_ipfs_url='dummy data', mint_gas_fee=0, mint_success=True, name="Test Name", title="Test Title", \
                         view_public=True, contract_id=1, token_id=1, image_web_url='dummy data'):
         
         start_bulk = 1
         #n_rows+=1       
         
         for n in range(start_bulk, n_rows + 1):
                         
            print("token: " + str(token_id) + " contract: " + str(contract_id))
            self.cur.execute("INSERT INTO erc721token (CREATED_BY, CREATED_DT, LAST_MODIFIED_BY, UPDATED_DT, DESCRIPTION, IPFS_IMAGE_CID, IMAGE_IPFS_URL, META_DATA, META_DATA_IPFS_CID, META_DATA_IPFS_URL," \
                             "MINT_GAS_FEE, MINT_SUCCESS, NAME, TITLE, VIEW_PUBLIC, CONTRACT_ID, TOKEN_ID, IMAGE_WEB_URL) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                                (createdby, datetime.now(), createdby, datetime.now(), description, ipfs_image_cid, image_ipfs_url, meta_data, meta_data_ipfs_cid, meta_data_ipfs_url, \
                                 mint_gas_fee, mint_success, name + " " + str(token_id), title + " " + str(token_id), view_public, contract_id, token_id, image_web_url))


    def add_token (self, createdby=102, created_dt=datetime.now(), last_modified_by=102, updated_dt=None, best_ask=0, best_bid=0,featured=True, public_view=True, chain_id=1, \
                    trending=True, active=True, fotd=True, n_rows=1):
        start_bulk= 1
         
        for n in range(start_bulk, n_rows + 1):
            self.cur.execute("INSERT INTO TOKEN (CREATED_BY, CREATED_DT, LAST_MODIFIED_BY, UPDATED_DT, BEST_ASK, BEST_BID, FEATURED, PUBLIC_VIEW, CHAIN_ID, TRENDING, ACTIVE, FOTD) " \
                            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (createdby, created_dt, last_modified_by, updated_dt, best_ask, best_bid, featured, public_view, chain_id, trending, active, fotd))
            

    def add_portfolio(self, created_by=102, created_dt=datetime.now(), last_modified_by=None, updated_dt=None, owner_id=0, token_id=0, n_rows=1):
        list_usrs     = []
        list_token_id = []
        
        start_bulk = 1
        
        self.cur.execute('select id from usr where user_name like \'%john%\' ')        
        for r in self.cur:
            usr_id = r[0]
            list_usrs.append(usr_id)


        self.cur.execute('select id from erc721token')
        for id in self.cur:
            it_token_id = id[0]
            list_token_id.append(it_token_id)            
        
        
        for n in range(start_bulk, n_rows + 1):
            owner_id = random.choice(list_usrs)
            token_id = random.choice(list_token_id)
            
            self.cur.execute("INSERT INTO PORTFOLIO(CREATED_BY, CREATED_DT, LAST_MODIFIED_BY, UPDATED_DT, OWNER_ID, TOKEN_ID) VALUES (%s,%s,%s,%s,%s,%s)",
                            (created_by, created_dt, last_modified_by, updated_dt, owner_id, token_id))

        
    def add_trades(self, created_by=102, created_dt=datetime.now(), last_modified_by=None, updated_dt=None, net_to_seller=0.002, platform_fee=0.0, successful=True, transaction_amount=0, \
                  buyer_id=0, seller_id=0, token_id=0, n_rows=1):
              
        start_bulk = 1
            
        list_usrs = []
        self.cur.execute('select id from usr ')        
        for r in self.cur:
            usr_id = r[0]
            list_usrs.append(usr_id)        
        
        list_owners = []
        self.cur.execute('select owner_id from portfolio ')        
        for r in self.cur:
            owner_id = r[0]
            list_owners.append(owner_id)

        list_token_id = []
        self.cur.execute('select id from token ')
        for id in self.cur:
            it_token_id = id[0]
            list_token_id.append(it_token_id) 

    
        for n in range(start_bulk, n_rows + 1):
            buyer_id     = random.choice(list_usrs)
            seller_id    = random.choice(list_owners)
            platform_fee = random.uniform(2.00, 20000.00)
            token_id     = random.choice(list_token_id)
            print(f'buyer_id {buyer_id} seller_id {seller_id} platform_fee {round(platform_fee,2)} token_id {token_id}')
            
            self.cur.execute("INSERT INTO TRADE(CREATED_BY, CREATED_DT, LAST_MODIFIED_BY, UPDATED_DT, NET_TO_SELLER, PLATFORM_FEE, SUCCESSFUL, TRANSACTION_AMOUNT, BUYER_ID, SELLER_ID, TOKEN_ID)" \
                            " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                            (created_by, created_dt, last_modified_by, updated_dt, net_to_seller, round(platform_fee,2), successful, transaction_amount, buyer_id, seller_id, token_id))
        
    
    def truncate_all(self):
        self.cur.execute('SELECT table_name FROM information_schema.tables WHERE table_schema=\'public\' AND table_type=\'BASE TABLE\'; ')
        for table in self.cur:
            self.cur.execute("truncate table " + table + " cascade;")

 

    def commit(self):
        self.conn.commit()
    def get_conn(self):
        load_dotenv(".env")
        dbname = os.environ.get('instamint_db_dbname')
        user = os.environ.get('instamint_db_user')
        pwd = os.environ.get('instamint_db_password')
        host = os.environ.get('instamint_db_host')
        port = os.environ.get('instamint_db_port')
        conn = psycopg.connect(dbname=dbname, user=user, password=pwd, host=host,port=port,sslmode='require')
        return conn
    
    
    profile_urls = [
    'https://preview.keenthemes.com/metronic8/demo3/assets/media/avatars/150-11.jpg',
    'https://preview.keenthemes.com/metronic8/demo3/assets/media/avatars/150-3.jpg',
    'https://preview.keenthemes.com/metronic8/demo3/assets/media/avatars/150-4.jpg',
    'https://preview.keenthemes.com/metronic8/demo3/assets/media/avatars/150-5.jpg',
    'https://preview.keenthemes.com/metronic8/demo3/assets/media/avatars/150-6.jpg',
    'https://s3.wasabisys.com/instamint-dev/246187869_254637129951783_225512577885539205_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246804666_323309386224407_5563681764716080390_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/210561601_493374595103923_1779031240527018461_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/244693907_116215967476386_6421037760491185533_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247452254_414944993489532_4571682700181802921_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247287438_396881648657550_5683201067676385149_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247020247_555872032184789_6239046034304340173_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246804402_370688021510828_7428926388780647323_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247448306_381216313446868_3082287690405353313_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247873877_331719512090792_4209664251653131853_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247464962_630328468376736_159476687614725114_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247149026_839955986691465_6609808753861066883_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/244440034_248756777205083_401270745966007888_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/244644199_375417414280575_4871279516845424569_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246775626_190153953238035_6860290339956084016_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247299442_1421444998250405_2858720919944745562_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247529741_448843430191085_5838958173993863523_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247470979_200999768823443_6032400720836484119_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247330746_1097248214419530_8809020395923081133_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246032520_1400479963683112_6297447483721108804_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247672194_427991952044862_840802432321254825_n.webp.jpg',
    'https://s3.wasabisys.com/instamint-dev/246760123_490108111963060_476841743450517676_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246976942_1027163141459030_4461846774584438937_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246142394_1497230963977931_6481627999928924925_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246713410_266394568741047_2207367077237240387_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247318754_2913062202339932_6430156364048478922_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247165947_407128657529020_6894655067734161268_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246849753_402805738159160_5377823605132133847_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247681889_558390418570238_3546328636901376923_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246996727_1028863631243363_8570530481028581597_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247084278_1258169494662243_1505542952318312258_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/244436778_578391643311143_8770598837988339598_n.webp.jpg',
    'https://s3.wasabisys.com/instamint-dev/246911420_3328131210753602_783991390533827321_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246791223_4332096823511681_5478026496058385298_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/234557278_4346656792083253_7211255658976116915_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246780658_220346460167513_32611685689579059_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/206094073_271488598101204_4571422527894048543_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/245256581_166065065718253_1623698814668328804_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/245273786_2900196210230616_1875806006227532584_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/248372190_456930649083359_8742621700755192827_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246038313_750007502476520_8587082036697972438_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246839290_2672341389579183_6750381841986439367_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246888369_1468776976849008_5080195778213535182_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246244529_412084610463678_2791129285817535909_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246500474_4348193038630619_3140460020113711090_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247392720_590349335491088_4966619795061246014_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/247581016_870510743834405_5090317932422528202_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/130174207_1037949136705597_3117354114884106502_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/69407341_911399185876865_1977591849546084868_n.jpg',
    'https://s3.wasabisys.com/instamint-dev/246894595_987198958516281_3487473656552913564_n.jpg']


