import time
import json
import requests
from progress.bar import IncrementalBar




token = open("private/token_vk").read()
# with open("private/token.txt", "r") as f: 
#     token_yan = f.read()
# user_id = "49591870",21278758.



class VK:
 
   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       
   def common_params(self):
       return {
           'access_token': self.token,
           'v': self.version
       }
   def get_profile_photo(self):
       params = self.common_params()
       params.update({"owner_id":self.id, "album_id": "profile","photo_sizes":"0","extended":"1"})
       response =requests.get('https://api.vk.com/method/photos.get', params=params)
       return response.json()
        
class YaUploader:

    url = "https://cloud-api.yandex.net/v1/disk/"

    def __init__(self, token: str):
        self.token = token
        
    def common_headers(self):
        return {
            "Authorization": "OAuth "+ self.token
        }
    def _build_url(self,api_method):
        return f"{self.url}{api_method}"
    
    def create_folder(self):
        params = {"path":f"/{vk.id}"}
        response = requests.put(self._build_url("resources"), headers=self.common_headers(), params=params) 

    def upload(self,paths,url):
        params = {"path": f"{vk.id}/{paths}.jpg", "url": f"{url}"} 
        response = requests.post(self._build_url("resources/upload"),params = params,headers = self.common_headers())

    def delete_folder(self):
        params = {"path": f"{vk.id}"}
        response = requests.delete(self._build_url("resources"), params = params, headers = self.common_headers())

    def get_spisok_files(self):
        response = requests.get(self._build_url("resources/files"), headers = self.common_headers())
        return response.json()
        
    def info_folder(self,path):
        params = {"path": f"/{path}"}
        response = requests.get(self._build_url("resources"),headers = self.common_headers(),params = params )
        return response.json()

if __name__ == '__main__':
    user_vk_id = input("Введите id пользователя: ")
    token_yan = input("Введите токен Полигона.Яндекс диска: ")
    

    vk = VK(token, user_vk_id)
    vk_photos = vk.get_profile_photo()


    uploader = YaUploader(token_yan)
    uploader.delete_folder()
    uploader.create_folder()
   
    url_href = []
    count = []
    for items in vk.get_profile_photo()["response"]["items"]:
        if items["likes"]["count"] not in count: 
            url_href.extend([{items["likes"]["count"]:size["url"] for size in items["sizes"] if size["type"] == "z"}])
            count.append(items["likes"]["count"])
        else:
            url_href.extend([{f"{items['likes']['count']} {items['date']}":size["url"] for size in items["sizes"] if size["type"] == "z"}])
            
        
    bar = IncrementalBar('Countdown', max = len(url_href))
    for href in url_href:
        bar.next()
        time.sleep(0.1)
        for name,url1 in href.items(): 
            uploader.upload(name,url1)   
    bar.finish()  
    


    info = [] 
    for item in uploader.info_folder(user_vk_id)['_embedded']['items']:
        print(item["name"])
        data = {
            "name": item['name'],
            "size": "z"
        }
        info.append(data)
    print(info)    
    with open("data.json", "w") as f:
        json.dump(info,f)



