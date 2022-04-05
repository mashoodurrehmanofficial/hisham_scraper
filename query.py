 


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


# FTX  Centralized

base_count = NftTable.objects.filter(nft='CloneX') 
child_count = DetailedExchangeTable.objects.filter(exchange='FTX  Centralized') 

print(base_count)
print(child_count.values())