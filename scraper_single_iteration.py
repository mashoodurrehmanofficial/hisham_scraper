# %%
 
from bs4 import BeautifulSoup
import requests,sys,pandas as pd,time,sqlalchemy ,json,traceback,os
from datetime import datetime

# %%

credentials = json.loads(open("./credentials.json",'r').read())
database_ip       = credentials['host']
database_username = credentials['username']
database_password = credentials['password']
database_name     = credentials['database']
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))

# %%
exchange_url = "https://www.coingecko.com/en/exchanges"
nft_url = "https://www.coingecko.com/en/nft"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36', 
}
 

# %%
def getNextPageIndex(soup):
    all_link_tags = soup.select("a.page-link")
    for link in all_link_tags:
        if link.has_attr("rel") and link['rel'][0]=="next":
            index = link['href'].split("=")[-1]
            return str(index).replace("'","").replace('"',"")
    return None

def formatString(text):
    return str(text).strip().replace("\n"," ").replace("\t","").replace("  "," ").replace("₿","$")


def startTimer(seconds=0):
    for remaining in range(seconds, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining)) 
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r\nNew Cycle\n")

# %%


# %%
# data_container = {"exchange_data":[],"nft_data":[]}
def getDataContainer():
    data_container = {"exchange_data":[],"nft_data":[]}
    for url in [exchange_url,nft_url][:]:
        catergory = 'exchange' if 'exchange' in str(url) else "nft"
        for index in range(1,100):
            print("-"*50)
            temp_url = url+ f'?page={index}'
            print(temp_url)
            res = requests.get(temp_url, headers=headers)
            print("-> Creating Soup")
            soup = BeautifulSoup(str(res.text), "lxml")
            print("-> Analyzing Rows")
            table_rows = soup.select("div.coingecko-table div.coin-table.table-responsive  table.table-scrollable tbody tr")
            table_rows = [[formatString(y.text) for y in x.select("td")][:-1] for x in table_rows] 
            if catergory=='exchange':
                data_container['exchange_data'] = data_container['exchange_data'] + table_rows
            else:
                data_container['nft_data'] = data_container['nft_data'] + table_rows
                
            if not getNextPageIndex(soup=soup):
                break
            
    for x in data_container:
        for index,row in enumerate(data_container[x][:]):
            data_container[x][index] = data_container[x][index] + [str(datetime.today())]
            
            
    return data_container          
            
        
        

# %%
# for x in data_container:
#     for index,row in enumerate(data_container[x][:]):
#         data_container[x][index] = data_container[x][index] + [str(datetime.today())]
#         # print(datetime.today())
#         print(data_container[x][index])

# %%
# exchange_df = pd.DataFrame(data=data_container['exchange_data'],columns=["index",'exchange','trust_score','total_24h_volume_normalized','total_24h_volume','visits_similarWeb','coins','pairs',"time_stamp"])
# nft_df = pd.DataFrame(data=data_container['nft_data'],columns=["index",'nft','floor_price','total_24h',"market_cap","total_24h_volume","owners","total_24h_owners","total_assets","time_stamp" ])

# exchange_df.to_sql(name="exchange", con=database_connection,if_exists='append', chunksize=1000,index=False)
# nft_df.to_sql(name="nft", con=database_connection,if_exists='append', chunksize=1000,index=False)

# %%
# print(exchange_df.columns)

# %%
def main():
    try:
        index=0
        while True:
            print("-> Scrapping started !")
            data_container = getDataContainer()
            print("-> Creating DataFrame")
            
            exchange_df = pd.DataFrame(data=data_container['exchange_data'],columns=["index",'exchange','trust_score','total_24h_volume_normalized','total_24h_volume','visits_similarWeb','coins','pairs',"time_stamp"])
            nft_df = pd.DataFrame(data=data_container['nft_data'],columns=["index",'nft','floor_price','total_24h',"market_cap","total_24h_volume","owners","total_24h_owners","total_assets","time_stamp" ])
            exchange_df.to_sql(name="exchange", con=database_connection,if_exists='append', chunksize=1000,index=False)
            nft_df.to_sql(name="nft", con=database_connection,if_exists='append', chunksize=1000,index=False)
            print("-> Data Saved to Database !")
            print("-"*50)
            # startTimer(seconds=20)
            index = index+1
            if index>0:break
    except Exception as e:
        print(traceback.print_exc())
        main()
    
     

# %%
main()

# %%



