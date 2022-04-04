 


import os,json
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()
# Now this script or any imported module can use any part of Django it needs.
from root.models import *
import datetime
from unidecode import unidecode

def stringify(text): 
    return unidecode(str(text))

    
    
    
def insertIntoMainTables(data_container):
    ExchangeTable.objects.all().delete()
    NftTable.objects.all().delete()  
    ExchangeTable.objects.bulk_create([
        ExchangeTable(
            detail_url=stringify(x[0]),
            rank=stringify(x[1]),
            exchange=stringify(x[2]),
            trust_score=stringify(x[3]),
            total_24h_volume_normalized=stringify(x[4]),
            total_24h_volume=stringify(x[5]),
            visits_similarWeb=stringify(x[6]),
            coins=stringify(x[7]),
            pairs=stringify(x[8]),
            image_url=stringify(x[-2]), 
            time_stamp=stringify(datetime.datetime.now())
        )
        for x in data_container['exchange_data'][:]
    ])
    NftTable.objects.bulk_create([
        NftTable(
            detail_url=stringify(x[0]),
            rank=stringify(x[1]),
            nft=stringify(x[2]),
            floor_price=stringify(x[3]),
            total_24h=stringify(x[4]),
            image_url=stringify(x[-2]), 

            market_cap=stringify(x[5]),
            total_24h_volume=stringify(x[6]),
            owners=stringify(x[7]),
            total_24h_owners=stringify(x[8]),
            total_assets=stringify(x[9]),
            time_stamp=stringify(datetime.datetime.now())
        )
        for x in data_container['nft_data'][:]
    ])
    
    print("ExchangeTable = ",ExchangeTable.objects.all().count())
    print("NftTable = ",NftTable.objects.all().count())





def insertIntoSubTables(detailed_data_container):
    DetailedExchangeTable.objects.all().delete()
    DetailedNftTable.objects.all().delete()
    
    
    exchange_container =[]
    index=0
    for key,val in detailed_data_container['exchange_data'].items():
        for child_row in val: 
            images = []
            try: 
                images = [x for x in child_row if type(x) is list][0]
            except:
                pass
            index=index+1
            exchange_container.append(
                DetailedExchangeTable( 
                    exchange = key ,
                    rank = stringify(child_row[0]  ) ,
                    coins = stringify(child_row[1]  ) ,
                    pairs = stringify(child_row[-9]  ) ,
                    price = stringify(child_row[-8]  ) ,
                    spread = stringify(child_row[-7]  ) ,
                    depth_positive_2 = stringify(child_row[-6]  ) ,
                    depth_negative_2 = stringify(child_row[-5]  ) ,
                    total_24h_volume = stringify(child_row[-4]  ) ,
                    volume_percentage = stringify(child_row[-3]  ) ,
                    last_traded = stringify(child_row[-2]  ) ,
                    image_url=stringify(images), 
                )
            ) 
    DetailedExchangeTable.objects.bulk_create(exchange_container)
    
    
     
    
    nft_container =[]
    index=0
    for key,val in detailed_data_container['nft_data'].items(): 
        nft_container.append(
            DetailedNftTable( 
                nft = key ,  
                floor_price = stringify(val['floor_price'] ) ,
                market_cap = stringify(val['market_cap'] ) ,
                total_24h_volume = stringify(val['total_24h_volume'] ) ,
                floor_price_usd = stringify(val['floor_price_usd']  ) ,
                floor_price_percentage = stringify(val['floor_price_percentage'] ) ,
                market_cap_usd = stringify(val['market_cap_usd'] ) ,
                market_cap_percentage = stringify(val['market_cap_percentage'] ) ,
                top_nfts_by_market_cap = stringify(val['top_nfts_by_market_cap'] ) ,
                stat_table_container = stringify(val['stat_table_container'] ) ,
            )
        ) 
      
    DetailedNftTable.objects.bulk_create(nft_container)
    print("DetailedExchangeTable = ",DetailedExchangeTable.objects.all().count())
    print("DetailedNftTable = ",DetailedNftTable.objects.all().count())
    
    
    
    
def checkStatus(): 
    print("ExchangeTable = ",ExchangeTable.objects.all().count())
    print("NftTable = ",NftTable.objects.all().count())
    print("DetailedExchangeTable = ",DetailedExchangeTable.objects.all().count())
    print("DetailedNftTable = ",DetailedNftTable.objects.all().count())
    
def clearDatabase():
    ExchangeTable.objects.all().delete()
    NftTable.objects.all().delete()
    DetailedExchangeTable.objects.all().delete()
    DetailedNftTable.objects.all().delete()
    
    
    
if __name__ == '__main__':
    # clearDatabase()
# 
    checkStatus()
    with open("res.json","r",encoding="utf-8")as file:
        data_container =  json.loads(file.read())
        
    with open("res2.json","r",encoding="utf-8")as file:
        detailed_data_container =  json.loads(file.read())

    
    # insertIntoMainTables(data_container)
    # insertIntoSubTables(detailed_data_container)