import os,json
dir_path = os.path.dirname(os.path.realpath(__file__))
credentials = json.loads(open(  os.path.join(dir_path,"credentials.json")  ,'r').read())
print(credentials)