from datetime import datetime
import re
import modules.database as db

def is_commercial(title, desc):
    is_comercial_title = "comercial" in title.lower()
    is_comercial_desc = "comercial" in desc.lower()
    # print("___________________")
    # if is_comercial_title: print(title.lower())
    # if is_comercial_desc: print(desc.lower())
    # print("___________________")
    if is_comercial_title or is_comercial_desc: return True
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
    return db.existing_entry(id)

def check_was_updated(id, update_date):
    if entry_exists(id) == 0: return True #If don't exists it will grab the rest of info
    last_updated = db.get_last_updated(id)
    match = str(update_date) == str(last_updated[0]) 

    return match is False #If don't match update the index, 

def exctract_listing_info(listing):
        listing_dict = {}
        listing_details = listing['listing']
        adress_info = listing_details['address']

        is_comercial = is_commercial(listing_details["title"], listing_details["description"])
        print(is_comercial, listing_details['id'] )
        if is_comercial is True: 
            comercial_dict = { 'listing' : {
                'id': listing_details['id'],
                'comercial': True
                }
            }
            return comercial_dict

        was_updated = check_was_updated(listing_details['id'] , listing_details['updatedAt'])
        if was_updated is False: return None

        listing_dict["id"] = listing_details['id'] 
        listing_dict["comercial"] = is_comercial
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
        listing_dict['link'] = listing['link']['href'] 
        listing_dict["visited"] = False
        
        return {'listing': listing_dict}