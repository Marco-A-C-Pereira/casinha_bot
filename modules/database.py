import json
import redis

r = redis.Redis(decode_responses=True)

print("\033c")

def save_results_from_master_list(master_list):
    with r.pipeline() as pipe:
        for listing in master_list: 
            listing_json = json.dumps(listing)

            pipe.json().set(listing['listing']['id'], '$', listing)

        pipe.execute()
    
    r.bgsave()

def get_listings():
    key = "2649699691"
    with r.pipeline() as pipe:
        pipe.json().get(key)
        dict_resp = json.loads(pipe.execute()[0])
        for i in dict_resp:
            print(dict_resp[i])

def existing_entry(id):
    return r.exists(id)

def get_last_updated(id):
    return r.json().get(id, "$..update_date")

# print(r.json().get("2624229581", "$..update_date"))