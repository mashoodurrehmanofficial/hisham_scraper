 
from bs4 import BeautifulSoup
import requests,sys,pandas as pd,time,sqlalchemy ,json
from datetime import datetime
credentials = json.loads(open("credentials.json",'r').read())
print(credentials)
credentials = json.loads(open("credentials.json",'r').read())
database_ip       = credentials['host']
database_username = credentials['username']
database_password = credentials['password']
database_name     = credentials['database']
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))

print(sqlalchemy.inspect(database_connection).has_table("BOOKS"))