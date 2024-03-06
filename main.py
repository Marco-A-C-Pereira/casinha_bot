import pprint

import modules.data_processing as dp
import modules.database as db
import modules.requests as rq
import modules.telegram_bot.bot_main as tele_bot

print("\033c")

pp = pprint.PrettyPrinter(indent=4)
LOCAL_MODE = False
master_list = []

def extract_listings():
    pagination = 0
    search_results = rq.request_list(pagination)['search']['result']['listings']

    
    for listing in search_results:
        try:
            formatted_data = dp.exctract_listing_info(listing)
            if formatted_data is not None:
                # pp.pprint(formatted_data['title'] + formatted_data['update_date'])
                master_list.append(formatted_data)
        except Exception as e: print(e)

    db.store_local_list(master_list)

def MAIN():
    # extract_listings()
    tele_bot.main()
    print("Finished ruinning")

MAIN()  