import math
import pprint
import time

import modules.data_processing as dp
import modules.database as db
import modules.requests as rq
import modules.telegram_bot.bot_main as tele_bot
import datetime

print("\033c")

pp = pprint.PrettyPrinter(indent=4)
master_list = []

def time_calculations(entry_date):

    formatted_entry = datetime.datetime.fromisoformat(entry_date).replace(tzinfo=None) 
    formatted_now = datetime.datetime.fromisoformat(datetime.datetime.now().isoformat())
    print(formatted_entry)
    print(formatted_now)


    total_difference = formatted_now - formatted_entry
    total_hours = total_difference.total_seconds() / 3600

    return math.ceil(total_hours)

def continue_pagination(last_result):
    if "title" not in last_result: return True
    
    if time_calculations(last_result["updatedAt"]) >= 24: return False
    local_list = db.request_local_list()
    if len(local_list) > 0:
        for local_item in local_list:
            if local_item["update_date"] == last_result["updatedAt"]: return False

    return True    

def extract_listings():
    pagination = 0
    last_result = {}
    should_paginate = continue_pagination(last_result) 
    print(continue_pagination(last_result))

    while(should_paginate is True):
        search_results = rq.request_list(pagination)['search']['result']['listings']

        print(f"page: {pagination} {len(search_results)} results")
        if len(search_results) != 0:
            last_result = search_results[-1]
            pagination = pagination + 1

            # Ultimo search_result bate com o mais recente locallist ? (data de update) ou é maior que 24h no formato iso 

            for listing in search_results:
                try:
                    formatted_data = dp.exctract_listing_info(listing)
                    if formatted_data is not None:
                        # pp.pprint(formatted_data['title'] + formatted_data['update_date'])
                        master_list.append(formatted_data)
                except Exception as e: print(e)

    db.store_local_list(master_list)



def MAIN():
    extract_listings()
    db.store_local_list(master_list)
    tele_bot.main()
    print("Finished ruinning")

MAIN()  