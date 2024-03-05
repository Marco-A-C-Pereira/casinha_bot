import pprint

import modules.data_processing as dp
import modules.database as db
import modules.requests as rq

print("\033c")

pp = pprint.PrettyPrinter(indent=4)
LOCAL_MODE = False
master_list = []

def extract_listings():
    if (not LOCAL_MODE):
        pagination = 0
        search_results = rq.request_list(pagination)['search']['result']['listings']
        db.store_small_list(search_results)

    listings = db.request_small_list() #Preciso mesmo ter essa segunda chamada ?

    for listing in listings[1:]:
        formatted_data = dp.exctract_listing_info(listing)
        if formatted_data is not None:
            # pp.pprint(formatted_data['title'] + formatted_data['update_date'])
            master_list.append(formatted_data)
            # dp.extract_images(formatted_data['id'], formatted_data['link'])

    db.store_local_list(master_list)

def MAIN():
    extract_listings()

MAIN()