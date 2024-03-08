import requests
from fake_useragent import UserAgent
import json


UA = UserAgent().random
BASE_URL = "https://www.zapimoveis.com.br"
SESSION = requests.Session()
request_header = {"User-Agent": UA,'X-Domain': '.zapimoveis.com.br'}

def request_list(index):
    request_url = f"https://glue-api.zapimoveis.com.br/v2/listings?user=793072f0-ece7-455a-a431-50b80e07f95f&portal=ZAP&includeFields=search%28result%28listings%28listing%28listingsCount%2CsourceId%2CdisplayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2Cstamps%2CcreatedAt%2Cfloors%2CunitTypes%2CnonActivationReason%2CproviderId%2CpropertyType%2CunitSubTypes%2CunitsOnTheFloor%2ClegacyId%2Cid%2Cportal%2CunitFloor%2CparkingSpaces%2CupdatedAt%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2CadvertiserContact%2CwhatsappNumber%2Cbedrooms%2CacceptExchange%2CpricingInfos%2CshowPrice%2Cresale%2Cbuildings%2CcapacityLimit%2Cstatus%2CpriceSuggestion%29%2Caccount%28id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2ClegacyZapId%2CcreatedDate%2Ctier%29%2Cmedias%2CaccountLink%2Clink%29%29%2CtotalCount%29%2Cpage%2Cfacets%2CfullUriFragments&categoryPage=RESULT&developmentsSize=0&superPremiumSize=0&business=RENTAL&sort=updatedAt+DESC&rentalPeriod=MONTHLY&parentId=null&listingType=USED&rentalTotalPriceMax=1000&rentTotalPrice=true&addressCity=Curitiba&addressLocationId=BR%3EParana%3ENULL%3ECuritiba&addressState=Paran%C3%A1&addressPointLat=-25.312814&addressPointLon=-49.299585&addressType=city&unitTypes=APARTMENT%2CAPARTMENT%2CAPARTMENT%2CHOME%2CHOME%2CHOME%2CHOME%2CAPARTMENT%2CAPARTMENT%2CAPARTMENT%2CALLOTMENT_LAND%2CFARM&unitTypesV3=APARTMENT%2CUnitType_NONE%2CKITNET%2CHOME%2CTWO_STORY_HOUSE%2CCONDOMINIUM%2CVILLAGE_HOUSE%2CPENTHOUSE%2CFLAT%2CLOFT%2CRESIDENTIAL_ALLOTMENT_LAND%2CFARM&unitSubTypes=UnitSubType_NONE%2CDUPLEX%2CTRIPLEX%7CSTUDIO%7CKITNET%7CUnitSubType_NONE%2CTWO_STORY_HOUSE%2CSINGLE_STOREY_HOUSE%2CKITNET%7CTWO_STORY_HOUSE%7CCONDOMINIUM%7CVILLAGE_HOUSE%7CPENTHOUSE%7CFLAT%7CLOFT%7CUnitSubType_NONE%2CCONDOMINIUM%2CVILLAGE_HOUSE%7CUnitSubType_NONE%2CCONDOMINIUM&usageTypes=RESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL&page={index}&size=15&from={index*15}&levels=CITY&ref=&__zt=mtc%3Adeduplication2023&images=undefined(A:Brand;v=24, Google"
    response = SESSION.get(request_url, headers=request_header)

    return response.json()
    # if response.status_code == 200: 

def request_json_list():
    f = open('smallList.json', encoding="utf-8")
    return json.load(f)

def request_listing_page(url):
    response = SESSION.get(url, headers=request_header)
    if response.status_code != 200: raise ValueError(429)  # noqa: E701


    return response
    # print(f"Status code {response.status_code} Retrying .... ")
    # time.sleep(10)

    # return request_listing_page(url)