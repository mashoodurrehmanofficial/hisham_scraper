from django.db import models
import datetime
from django.conf import settings
from pytz import timezone 
from datetime import  datetime
from  django.utils.timezone import  now
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver


# Create your models here.


class ExchangeTable(models.Model):  
    detail_url = models.CharField(max_length=500,default='',blank=True) 
    image_url = models.CharField(max_length=500,default='',blank=True) 
    
    rank = models.CharField(max_length=500,default='',blank=True) 
    exchange = models.CharField(max_length=500,default='',blank=True) 
    trust_score = models.CharField(max_length=500,default='',blank=True) 
    total_24h_volume_normalized = models.CharField(max_length=500,default='',blank=True) 
    total_24h_volume = models.CharField(max_length=500,default='',blank=True) 
    visits_similarWeb = models.CharField(max_length=500,default='',blank=True) 
    coins = models.CharField(max_length=500,default='',blank=True) 
    pairs = models.CharField(max_length=500,default='',blank=True) 
    time_stamp = models.CharField(max_length=500,default='',blank=True)  
    
 
class NftTable(models.Model):  
    detail_url = models.CharField(max_length=500,default='',blank=True) 
    image_url = models.CharField(max_length=500,default='',blank=True) 
    rank = models.CharField(max_length=500,default='',blank=True) 
    nft = models.CharField(max_length=500,default='',blank=True)  
    floor_price = models.CharField(max_length=500,default='',blank=True)  
    total_24h = models.CharField(max_length=500,default='',blank=True)  
    market_cap = models.CharField(max_length=500,default='',blank=True)  
    total_24h_volume = models.CharField(max_length=500,default='',blank=True)  
    owners = models.CharField(max_length=500,default='',blank=True)  
    total_24h_owners = models.CharField(max_length=500,default='',blank=True)  
    total_assets = models.CharField(max_length=500,default='',blank=True)  
    time_stamp = models.CharField(max_length=500,default='',blank=True)     
 
 
class DetailedExchangeTable(models.Model):  
    exchange = models.CharField(max_length=500,default='',blank=True) 
    image_url = models.CharField(max_length=500,default='',blank=True) 
    rank = models.CharField(max_length=500,default='',blank=True) 
    coins = models.CharField(max_length=500,default='',blank=True) 
    pairs = models.CharField(max_length=500,default='',blank=True) 
    price = models.CharField(max_length=500,default='',blank=True) 
    spread = models.CharField(max_length=500,default='',blank=True) 
    depth_positive_2 = models.CharField(max_length=500,default='',blank=True) 
    depth_negative_2 = models.CharField(max_length=500,default='',blank=True) 
    total_24h_volume = models.CharField(max_length=500,default='',blank=True) 
    volume_percentage = models.CharField(max_length=500,default='',blank=True) 
    last_traded = models.CharField(max_length=500,default='',blank=True)  
    parent = models.ForeignKey(ExchangeTable,on_delete=models.CASCADE, null=True,blank=True)

class DetailedNftTable(models.Model):  
    nft = models.CharField(max_length=500,default='',blank=True) 
    floor_price = models.CharField(max_length=500,default='',blank=True)  
    market_cap = models.CharField(max_length=500,default='',blank=True)  
    total_24h_volume = models.CharField(max_length=500,default='',blank=True)  
    floor_price_usd = models.CharField(max_length=500,default='',blank=True)  
    floor_price_percentage = models.CharField(max_length=500,default='',blank=True)  
    market_cap_usd = models.CharField(max_length=500,default='',blank=True)  
    market_cap_percentage = models.CharField(max_length=500,default='',blank=True)  
    top_nfts_by_market_cap = models.TextField(default='',blank=True)  
    stat_table_container = models.TextField(default='',blank=True)   
    parent = models.ForeignKey(NftTable,on_delete=models.CASCADE, null=True,blank=True)