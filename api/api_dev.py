import requests
import json

test_usernames = {0: "56ms", 1: "nonbunary", 2: "poroknights",
                  3: "UrMinecraftDoggo", 4: "Skezza", 5: "kori_100",
                  6: "XD_Zaptro_XD", 7: "seattle72", 8: "Refraction"}

user = 0
username = test_usernames[user]


#a = requests.get("https://api.hypixelskyblock.de/api/v1/cb/pages/balt")

username = "ycarusishere"
#username = "KebabOnNaan"
#username = "ItzAlpha__"
#username = "balt"
#username = "455fcc3f87ea4a92a6c38e190c39d8ec"
username = "56ms"
username = "Refraction"
#username = "seattle72"
#username = "Skezza"

ip = "127.0.0.1"  #  For running locally
#ip = "db.superbonecraft.dk"  # For the server

a = requests.get(f"http://{ip}:8000/pages/{username}")
#a = requests.get(f"http://{ip}:8000/total/Skezza")

#a = requests.get(f"{ip}/groups/56ms")
#a = requests.get(f"{ip}/total/15h")
#a = requests.get(f"{ip}/total/Larucus")
print(a.status_code)
print(a.json())

'''
#r = requests.get(f"http://127.0.0.1:8000/debug/56ms")
#r = requests.get(f"http://127.0.0.1:8000/debug/Refraction")
#r = requests.get(f"http://127.0.0.1:8000/debug/XD_Zaptro_XD")
print(r.status_code)
print(r.json())

for key, value in r.json().items():
    print (key+":", value)
#'''

'''
r = requests.get("http://127.0.0.1:8000/pages/56ms")
print(r.status_code)
#print(r.text)
print(r.json())#["inventory"]["prices"])#["inventory"]["prices"][0])
#'''
