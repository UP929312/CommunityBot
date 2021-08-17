import requests

from data.decode_container import parse_container

with open("data/hypixel_api_key.txt", 'r') as file:
    API_KEY = file.read()

#=======================================================

def get_data(username):

    try:        
        if len(username) <= 16:
            uuid_request = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
            if uuid_request.status_code != 200:
                return None, None
            uuid = uuid_request.json()["id"]
        else:
            uuid = username

        #print(uuid)
        
        profile_list = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}").json()
        #print(profile_list.keys())
        if not profile_list or profile_list.get("profiles") is None or profile_list == {'success': True, 'profiles': None}:
            print("# Error, profile parsing error. Possible wrong username?")
            return None, None
        if profile_list == {'success': False, 'cause': 'Invalid API key'}:
            print("Data/utils: Invalid API key, apparently?")
            return None, None
        
        valid_profiles = [x for x in profile_list["profiles"] if "last_save" in x['members'][uuid]]        
        profile = max(valid_profiles, key=lambda x: x['members'][uuid]['last_save'])
        player_data = profile["members"][uuid]; other_data = profile

    except Exception as e:
        print("######", e)
        return None, None

    return player_data, other_data

def get_storage(player_data):
    storage_items = []
    if not player_data.get("backpack_contents", False):
        return []
    for i in range(0, 19):
        page = player_data["backpack_contents"].get(str(i), {"data": []})
        storage_items.extend(parse_container(page["data"]))
    return storage_items
