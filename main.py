import requests
import json
import pprint
from fake_useragent import UserAgent

import modules.data_processing as dp
import modules.requests as rq
import modules.database as db

print("\033c")

pp = pprint.PrettyPrinter(indent=4)
UA = UserAgent().random
BASE_URL = "zapimoveis.com.br"
SESSION = requests.Session()
TESTING_MODE = True
master_list = []

def request_json_list():
    f = open('smallList.json', encoding="utf-8")
    return json.load(f)

def request_list(index):
    request_url = f"https://glue-api.zapimoveis.com.br/v2/listings?user=d470fe2e-0257-43ce-97aa-895b3e843414&portal=ZAP&includeFields=search%28result%28listings%28listing%28listingsCount%2CsourceId%2CdisplayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2Cstamps%2CcreatedAt%2Cfloors%2CunitTypes%2CnonActivationReason%2CproviderId%2CpropertyType%2CunitSubTypes%2CunitsOnTheFloor%2ClegacyId%2Cid%2Cportal%2CunitFloor%2CparkingSpaces%2CupdatedAt%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2CadvertiserContact%2CwhatsappNumber%2Cbedrooms%2CacceptExchange%2CpricingInfos%2CshowPrice%2Cresale%2Cbuildings%2CcapacityLimit%2Cstatus%2CpriceSuggestion%29%2Caccount%28id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2ClegacyZapId%2CcreatedDate%2Cminisite%2Ctier%29%2Cmedias%2CaccountLink%2Clink%29%29%2CtotalCount%29%2Cpage%2Cfacets%2CfullUriFragments&categoryPage=RESULT&developmentsSize=0&superPremiumSize=0&__zt&business=RENTAL&sort=updatedAt+DESC&rentalPeriod=MONTHLY%2CYEARLY&parentId=null&listingType=USED&rentalTotalPriceMax=1000&rentTotalPrice=true&addressCity=Curitiba&addressLocationId=BR%3EParana%3ENULL%3ECuritiba&addressState=Paran%C3%A1&addressPointLat=-25.437238&addressPointLon=-49.269973&addressType=city&page=1&size=15&from={index}&levels=CITY&ref"
    request_header = {"User-Agent": UA,'X-Domain': '.zapimoveis.com.br'}
    response = SESSION.get(request_url, headers=request_header)

    return response.json()

def extract_listings():
    if (not TESTING_MODE):
        pagination = 0
        search_results = request_list(pagination)
        listings = search_results['search']['result']['listings']

        with open('smallList.json', 'w') as f:
            json.dump(listings, f)
            print("Wrote to Json KEK")

    listings = request_json_list()

    for listing in listings:
        listing_dict = {}
        listing_details = listing['listing']
        is_comercial = dp.is_commercial(listing_details["title"], listing_details["description"])
        was_updated = dp.was_updated(listing_details['id'] , listing_details['updatedAt'])

        listing_dict["id"] = listing_details['id'] 
        listing_dict["comercial"] = is_comercial
        
        if was_updated is False: continue
        if listing_dict["comercial"] is True: 
            master_list.append(listing_dict)
            continue

        listing_dict["title"] = listing_details['title'] 
        listing_dict["description"] = listing_details['description'] 

        listing_dict['whats'] = dp.format_phone(listing_details['whatsappNumber']) 
        listing_dict['creation_date'] = listing_details['createdAt']
        listing_dict['update_date'] = listing_details['updatedAt']
        listing_dict["total_monthly_price"] = listing_details['pricingInfos'][0]['rentalInfo']['monthlyRentalTotalPrice']
        
        listing_dict['bedrooms'] = dp.bedrooms(listing_details)

        adress_info = listing_details['address']
        listing_dict["city"] = adress_info['city']
        listing_dict["neighborhood"] = adress_info['neighborhood']
        listing_dict["street"] = adress_info['street']
        listing_dict["number"] = dp.street_number(adress_info)
        listing_dict["geo"] = dp.maps_point(adress_info)
        listing_dict['link'] = listing['link']['href'] 
        listing_dict["visited"] = False

        master_list.append({'listing': listing_dict})

        # for i in listing_dict:
        #     print('__________') 
        #     print(f"{i}: {listing_dict[i]}")

    db.save_results_from_master_list(master_list)

extract_listings()
# db.get_listings()
    