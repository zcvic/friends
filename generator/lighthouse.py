# -*- coding: utf-8 -*-
import requests
import json,os
import config
def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()

cfg=config.load()
filter = cfg['issues']
url = "https://api.github.com/repos/"+filter["repo"]+"/issues" 
res = requests.get(url).json()
for key in range(len(res)):
    print(res[key]['id'])
    id = res[key]['number']
    site = "{"+getmidstring(res[key]['body'],"{","}")+"}"    
    tempsite = json.loads(site)
    siteurl = tempsite["url"]
    print(tempsite["url"])
    if len(res[key]["labels"]) == 0:
       os.system(f"lighthouse {siteurl} --output html --locale zh --output-path ./public/site–{id}.html")      
       headers = {'Authorization': 'token '+ os.environ["GITHUB_TOKEN"]}
       url = "https://api.github.com/repos/"+filter["repo"]+"/issues/"+str(id)+"/comments"
       Test_Url =filter["link"]+"/public/site–"+str(id)+".html"  
       post_data = {"body":"LightHouse Testing Ok,Then Go [there]("+Test_Url+")"}
       print('res',url,headers,post_data)      
       print("comments",requests.post(url,headers=headers, data=json.dumps(post_data)))
       url = "https://api.github.com/repos/"+filter["repo"]+"/issues/"+str(id)+"/labels"
       post_data = {"labels":["suspend"]}
       print('res',url,headers,post_data)      
       print("changeLabels",requests.post(url,headers=headers, data=json.dumps(post_data)))