import requests
from fake_useragent import UserAgent
import json
from bs4 import BeautifulSoup


UA = UserAgent().random
BASE_URL = "https://www.zapimoveis.com.br"
SESSION = requests.Session()
request_header = {"User-Agent": UA,'X-Domain': '.zapimoveis.com.br'}

def request_list(index):
    request_url = f"https://glue-api.zapimoveis.com.br/v2/listings?user=d470fe2e-0257-43ce-97aa-895b3e843414&portal=ZAP&includeFields=search%28result%28listings%28listing%28listingsCount%2CsourceId%2CdisplayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2Cstamps%2CcreatedAt%2Cfloors%2CunitTypes%2CnonActivationReason%2CproviderId%2CpropertyType%2CunitSubTypes%2CunitsOnTheFloor%2ClegacyId%2Cid%2Cportal%2CunitFloor%2CparkingSpaces%2CupdatedAt%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2CadvertiserContact%2CwhatsappNumber%2Cbedrooms%2CacceptExchange%2CpricingInfos%2CshowPrice%2Cresale%2Cbuildings%2CcapacityLimit%2Cstatus%2CpriceSuggestion%29%2Caccount%28id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2ClegacyZapId%2CcreatedDate%2Cminisite%2Ctier%29%2Cmedias%2CaccountLink%2Clink%29%29%2CtotalCount%29%2Cpage%2Cfacets%2CfullUriFragments&categoryPage=RESULT&developmentsSize=0&superPremiumSize=0&__zt&business=RENTAL&sort=updatedAt+DESC&rentalPeriod=MONTHLY%2CYEARLY&parentId=null&listingType=USED&rentalTotalPriceMax=1000&rentTotalPrice=true&addressCity=Curitiba&addressLocationId=BR%3EParana%3ENULL%3ECuritiba&addressState=Paran%C3%A1&addressPointLat=-25.437238&addressPointLon=-49.269973&addressType=city&page=1&size=15&from={index}&levels=CITY&ref"
    response = SESSION.get(request_url, headers=request_header)

    return response.json()

def request_json_list():
    f = open('smallList.json', encoding="utf-8")
    return json.load(f)

def request_listing_page(url):
    response = SESSION.get(url, headers=request_header)

    return response