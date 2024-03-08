import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

def request_small_list():
    f = open('storage/smallList.json', encoding="utf-8")
    return json.load(f)

def store_small_list(master_dict):
        print("There are ", len(master_dict), " new entries in the temp list")
        with open('storage/smallList.json', 'w') as f:
            json.dump(master_dict, f)

def request_local_list():
    f = open('storage/localList.json', encoding="utf-8")
    return json.load(f)

def store_local_list(master_dict):
        print("There are ", len(master_dict), " new entries in the local list")
        local_list = request_local_list()
        combined_list = local_list + [listing for listing in master_dict if listing not in local_list]
        with open('storage/localList.json', 'w') as f:
            json.dump(combined_list, f)

def find_index(id):
    for index, listing in enumerate(request_local_list()):
        if listing["id"] == id:
            return index
    return None
    

def remove_from_list(index):
    loaded_list = request_local_list()
    del loaded_list[index]
    store_local_list(loaded_list) 