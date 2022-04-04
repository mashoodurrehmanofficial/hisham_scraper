from bs4 import BeautifulSoup
import requests,sys,pandas as pd,time,sqlalchemy ,json,os,django
from datetime import datetime
import itertools,django,os,json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup() 
from root.models import *

try:
    from connection import *
except:
    from .connection import *
    
    
from forex_python.bitcoin import BtcConverter
b = BtcConverter()
usd_unit = b.convert_btc_to_cur(1, 'USD')


domain = "https://www.coingecko.com"
exchange_url = "https://www.coingecko.com/en/exchanges"
nft_url = "https://www.coingecko.com/en/nft"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36', 
}


def getNextPageIndex(soup):
    all_link_tags = soup.select("a.page-link")
    for link in all_link_tags:
        if link.has_attr("rel") and link['rel'][0]=="next":
            index = link['href'].split("=")[-1]
            return str(index).replace("'","").replace('"',"")
    return None

def formatString(text):
    text =  str(text).strip().replace("\n"," ").replace("\t","").replace("  "," ") 
    if "₿" in text:
        text = text[1:] 
        text = text if len(str(text))>0 else '0'
        # print("text  = ",text)
        
        text = text.replace("'","").replace('"','').split(" ")[0]
        text =   usd_unit* float(text[:])
        text = "$" + '{:,}'.format(text)
    return text


def startTimer(seconds=0):
    for remaining in range(seconds, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining)) 
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r\nNew Cycle\n")



 
def getDataContainer(): 
    data_container = {"exchange_data":[],"nft_data":[]}
    for url in [exchange_url,nft_url][:]: 
    
        catergory = 'exchange' if 'exchange' in str(url) else "nft"
        for index in range(1,100):
            print("-"*50) 
            temp_url = exchange_url if catergory=='exchange'else nft_url   + f'?page={index}'
            temp_url = temp_url + f'?page={index}'
            print(temp_url)
            res = requests.get(temp_url, headers=headers)
            print("-> Creating Soup")
            soup = BeautifulSoup(str(res.text), "lxml")
            print("-> Analyzing Rows") 
            table_rows = soup.select("div.coingecko-table div.coin-table.table-responsive  table.table-scrollable tbody tr")
            table_rows = [   [y for y in x.select("td") ][:]   for x in table_rows] 
            
            for row_index,row in enumerate(table_rows):
                image = ([x.select("td img") for x in row])
                image = [x for x in image if x][0][0]['src'] 
                for td_index,td in enumerate(row[:]):
                    table_rows[row_index][td_index] = formatString(td.text)
                    if td_index==1:
                        url = formatString(td.text) if not td.select("span.pt-2.flex-column a") else domain+td.select("span.pt-2.flex-column a")[0]['href']
                        if 'http' not in url:
                            url = formatString(row[td_index]) if not td.select("a") else domain+td.select("a")[0]['href']
                        table_rows[row_index][0] = [table_rows[row_index][0],url]
                table_rows[row_index].append(image)
                
                            
            table_rows = [   [y for y in x if len(y)>0][:]   for x in table_rows] 
            
            
            for row_index,ow in enumerate(table_rows):
                temp = table_rows[row_index][0] 
                del table_rows[row_index][0] 
                table_rows[row_index].insert(0,temp[1] )   
                table_rows[row_index].insert(1,temp[0] )  
            
            print(f"total row on {index} = ", len(table_rows))
            
            if catergory=='exchange':
                data_container['exchange_data'] = data_container['exchange_data'] + table_rows
            else:
                data_container['nft_data'] = data_container['nft_data'] + table_rows
                
            if not getNextPageIndex(soup=soup):
                print("No next page")
                break
    print("before saving - data_container['exchange_data'] = ", len(data_container['exchange_data']))       
    for x in data_container:
        for index,row in enumerate(data_container[x][:]):
            data_container[x][index] = data_container[x][index] + [str(datetime.datetime.now())]
            
    with open("res.json","w",encoding="utf-8")as file:
        json.dump(data_container,file,indent=4)      
    return data_container          
            



def getDetailNftData(soup):
    top_bar = soup.select("dl.tw-mt-5.tw-grid")[0]
    top_bar_bold_text = [formatString(x.text) for x in top_bar.select("dd.tw-mt-1.tw-text-3xl.tw-font-semibold.tw-text-gray-900")]
    top_bar_lower_text = [formatString(x.text) for x in top_bar.select("span.tw-text-gray-500.tw-text-xl")]
    floor_price = top_bar_bold_text[0]
    market_cap = top_bar_bold_text[1]
    total_24h_volume = top_bar_bold_text[-1]
    floor_price_usd = top_bar_lower_text[0].split(" ")[0]
    floor_price_percentage = top_bar_lower_text[0].split(" ")[-1]
    market_cap_usd = top_bar_lower_text[-1].split(" ")[0]
    market_cap_percentage = top_bar_lower_text[-1].split(" ")[-1]
    top_nfts_by_market_cap = soup.select("a.text-secondary.ml-2.mb-3.col-10.d-block")
    top_nfts_by_market_cap = [ formatString(x.text) for x in top_nfts_by_market_cap]

    stat_table_container = {}
    stat_table = soup.select("div.table-responsive table.table")[0]
    stat_table_container['head'] = [formatString(x.text) for x in stat_table.select("thead tr th")]
    stat_table_container['body'] = [[formatString(y.text) for y in  x.select("td")] for x in stat_table.select("tbody tr")]

    return {
        "floor_price": floor_price,
        "market_cap": market_cap,
        "total_24h_volume": total_24h_volume,
        "floor_price_usd": floor_price_usd,
        "floor_price_percentage": floor_price_percentage,
        "market_cap_usd": market_cap_usd,
        "market_cap_percentage": market_cap_percentage,
        "top_nfts_by_market_cap": top_nfts_by_market_cap,
        "stat_table_container": stat_table_container, 
    }

        



def getDetailedDataContainer(data_container):
    detailed_data_container = {}
    for category,data in data_container.items():
        category_name = category.split("_")[0]
        detailed_data_container[category] = {}
        print("-"*50)
        print("category_name = ", category_name)
        if category_name=="exchange":
            for index,row in enumerate(data[:]):
                trade_name = row[2]
                url = row[0]
                print("Index = ",index)
                print(url) 
                res = requests.get(url)
                soup = BeautifulSoup(str(res.text),"lxml")
                trs = soup.select("table tbody tr")
                tds = [[ formatString(y.text) for y in x.select("td")] for x in trs]
                tds = [[y for y in x if len(y)>0 ]for x in tds if len(x)>10]
                
                tds_images = [x.select("td img") for x in trs]
                tds_images = [ [y['src'] for y in x] for x in tds_images]
                tds_images = [x for x in tds_images if x]
                for row_index,row in enumerate(tds_images):
                    try: tds[row_index].append(row) 
                    except:  pass
                
                
                
                detailed_data_container[category][trade_name] = tds
            pass      
        else:
            for index,row in enumerate(data[:]):
                trade_name = row[2]
                url = row[0] 
                print("Index = ",index)
                print(url) 
                res = requests.get(url)
                soup = BeautifulSoup(str(res.text),"lxml")
                detailed_data_container[category][trade_name] = getDetailNftData(soup)

    with open("res2.json","w",encoding="utf-8")as file:
        json.dump(detailed_data_container,file,indent=4)   
    return detailed_data_container              
            
            
            




 

def main():
    # try:
        index=0
        while True:
            print("-> Scrapping started Main Pages!")
            data_container = getDataContainer()
            insertIntoMainTables(data_container)
            # data has been saved to res.json 
            print("-> Scrapping started Sub-Level Pages!")
            # detailed_data_container = getDetailedDataContainer(data_container)
            # insertIntoSubTables(detailed_data_container)
            # print("-> Data Saved to Database !")
            print("-"*50)
            # startTimer(seconds=5)
            index = index+1
       
            break
    # except:
    #     main()
        
        
main()