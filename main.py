import math
import pprint

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

def continue_pagination(last_results, page_number):
    try:
        if page_number == 0: return True  # noqa: E701
        if len(last_results) < 15: return False  # noqa: E701

        older_than_day = time_calculations(last_results[-1]["updatedAt"]) >= 24 
        if older_than_day: return False  # noqa: E701

        local_list = db.request_local_list()
        if len(local_list) > 0:
            for local_item in local_list:
                if local_item["update_date"] == last_results[-1]["updatedAt"]: return False  # noqa: E701

        return True    
    except Exception as e: 
        print(f"Error in the continue pagination: {e}")  # noqa: E701
        return False


def extract_listings():
    pagination = 0
    last_results = []

    while(continue_pagination(last_results, pagination) is True):
        search_results = rq.request_list(pagination)['search']['result']['listings']
        print(f"page: {pagination} {len(search_results)} results")

        if len(search_results) != 0:
            last_results = search_results
            pagination = pagination + 1

            for listing in search_results:
                try:
                    formatted_data = dp.exctract_listing_info(listing)
                    if formatted_data is not None: master_list.append(formatted_data)  # noqa: E701
                
                except Exception as e: 
                    if e == "429": return # noqa: E701
                    print(f"Error in the data extracting phase {e}")  

    db.store_local_list(master_list)



def MAIN():
    # extract_listings()
    tele_bot.main()
    print("Finished ruinning")

MAIN()  