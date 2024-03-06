from datetime import datetime
import pprint
import re
from pathlib import Path
import shutil

import requests
import modules.database as db
import modules.requests as rq
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4)

def is_commercial(title, desc, link):
    banned_words = ["comercial", "loja"]

    for text in [title, desc, link]:
        if any(banned_word in text.lower() for banned_word in banned_words):
            # print(f"MATCH ! {text}")
            return True

    # is_comercial_title = "comercial" in title.lower()
    # is_comercial_desc = "comercial" in desc.lower()
    # is_comercial_link = "comercial" in link.lower()
    # if is_comercial_title or is_comercial_desc or is_comercial_link: return True
    return False
    
def add_leading_zero(number):
    str_number = str(number)
    
    return '0' + str_number if len(str_number) == 1 else str_number

def format_iso_date(iso_string):
    treated_date_obj = datetime.fromisoformat(iso_string)
    treated_date_str = f"{add_leading_zero(treated_date_obj.day)}/{add_leading_zero(treated_date_obj.month)}/{treated_date_obj.year}"

    return treated_date_str

def format_total_rent_info(json):
    treated_pricing_info = f"R$ {json['pricingInfos'][0]['rentalInfo']['monthlyRentalTotalPrice']}"
    return treated_pricing_info

def format_phone(whats):
    is_zero = len(whats) == 0
    is_repeated = all(number == whats[0] for number in whats)

    if is_zero or is_repeated: return "None"
    return re.sub(r'(\d{2})(\d{4})(\d{4})', r'(\1) \2-\3', whats)

def street_number(dict):
    return dict['streetNumber'] if "streetNumber" in dict else "????"

def maps_point(dict): 
    return dict['point'] if "point" in dict else "????"

def bedrooms(dict):
   return dict['bedrooms'][0] if len(dict['bedrooms']) != 0 else 0

def entry_exists(id):
        return list(filter(lambda local_listing: local_listing['id'] == id,db.request_local_list())) #Operação custosa

def exctract_listing_info(listing):
        listing_dict = {}
        listing_details = listing['listing']
        adress_info = listing_details['address']
        BASE_URL = "https://www.zapimoveis.com.br"

        if is_commercial(listing_details["title"], listing_details["description"],listing['link']['href']) is True: return None
        if len(entry_exists(listing_details['id'])) != 0:
            db.remove_from_list(db.find_index(listing_details['id'])) 

        # Solução mais elegante com Pandas ? Dataframe Filter ? 

        listing_dict["id"] = listing_details['id'] 
        listing_dict["title"] = listing_details['title'] 
        listing_dict["description"] = listing_details['description'] 
        listing_dict['whats'] = format_phone(listing_details['whatsappNumber']) 
        listing_dict['creation_date'] = listing_details['createdAt']
        listing_dict['update_date'] = listing_details['updatedAt']
        listing_dict["total_monthly_price"] = listing_details['pricingInfos'][0]['rentalInfo']['monthlyRentalTotalPrice']
        listing_dict['bedrooms'] = bedrooms(listing_details)
        listing_dict["city"] = adress_info['city']
        listing_dict["neighborhood"] = adress_info['neighborhood']
        listing_dict["street"] = adress_info['street']
        listing_dict["number"] = street_number(adress_info)
        listing_dict["geo"] = maps_point(adress_info)
        listing_dict['link'] = BASE_URL+listing['link']['href'] 
        listing_dict["visited"] = False
        
        return listing_dict

def extract_images(id, url):
    raw = rq.request_listing_page(url)
    page = BeautifulSoup(raw.text, "html.parser")
    carousel_container = page.select("#listing-carousel")[0]
    carousel_items = carousel_container.find_all('img')

    incrementer = 0
    path = f"storage/images/{id}"
    Path(path).mkdir(parents=True, exist_ok=True)

    for item in carousel_items[:3]:
        raw_img_url = item['srcset']
        formatted_url = raw_img_url.split("'")[0].split(" ")[0]

        incrementer += 1
        with open (f"{path}/{incrementer}.jpg", 'wb') as f:
            f.write(requests.get(formatted_url).content)