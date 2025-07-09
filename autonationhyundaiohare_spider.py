import requests
import json
import time

url = "https://www.autonationhyundaiohare.com/api/widget/ws-inv-data/getInventory"

headers = {
    "accept": "*/*",
    "content-type": "application/json",
    "origin": "https://www.autonationhyundaiohare.com/",
    "referer": "https://www.autonationhyundaiohare.com/all-inventory/index.htm",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

base_payload = {
    "siteId": "autonationhyundaiohare",
    "locale": "en_US",
    "device": "DESKTOP",
    "pageAlias": "INVENTORY_LISTING_DEFAULT_AUTO_NEW",
    "pageId": "autonationhyundaiohare_SITEBUILDER_INVENTORY_SEARCH_RESULTS_AUTO_NEW_V1_1",
    "windowId": "inventory-data-bus2",
    "widgetName": "ws-inv-data",
    "inventoryParameters": {},
    "preferences": {
        "pageSize": "18",
        "listing.config.id": "auto-all",
        "listing.boost.order": "account,make,model,bodyStyle,trim,optionCodes,modelCode,fuelType",
        "removeEmptyFacets": "true",
        "removeEmptyConstraints": "true",
        "displayerInstanceId": "",
        "required.display.sets": "TITLE,IMAGE_ALT,IMAGE_TITLE,PRICE,FEATURED_ITEMS,CALLOUT,LISTING,HIGHLIGHTED_ATTRIBUTES",
        "required.display.attributes": "accountCity,accountCountry,accountId,accountName,accountState,accountZipcode,askingPrice,attributes,autodataCaId_att_data,bed,bodyStyle,cab,carfaxIconUrl,carfaxIconUrlBlackWhite,carfaxUrl,carfaxValueBadgeAltText,categoryName,certified,chromeId_att_data,cityMpg,classification,classificationName,comments,courtesy,cpoChecklistUrl,daysOnLot,dcpaisVideoToken_att_data,deliveryDateRange,doors,driveLine,ebayAuctionId,eleadPrice,eleadPriceLessOEMCash,engine,engineSize,equipment,extColor,exteriorColor,fuelType,globalVehicleTrimId,gvLongTrimDescription,gvTrim,hasCarFaxReport,hideInternetPrice,highwayMpg,id,incentives,intColor,interiorColor,interiorColorCode,internetComments,internetPrice,inventoryDate,invoicePrice,isElectric_att_b,key,location,make,marketingTitle,mileage,model,modelCode,msrp,normalExteriorColor,normalFuelType,normalInteriorColor,numSaves,odometer,oemSerialNumber,oemSourcedMerchandisingStatus,optionCodes,options,packageCode,packages_internal,parent,parentId,paymentMonthly,payments,primary_image,propertyDescription,retailValue,saleLease,salePrice,sharedVehicle,status,stockNumber,transmission,trim,trimLevel,type,uuid,video,vin,warrantyDescription,wholesalePrice,year",
        "required.display.attributes.extra": "autonationCustomerCash_att_data",
        "facetInstanceId": "listing",
        "geoLocationEnabled": "false",
        "defaultGeoDistRadius": "0",
        "geoRadiusValues": "0,5,25,50,100,250,500,1000",
        "showCertifiedFranchiseVehiclesOnly": "false",
        "showFranchiseVehiclesOnly": "true",
        "extraFranchisesForUsedWindowStickers": "",
        "suppressAllConditions": "compliant",
        "violateUsedCompliance": "false",
        "showOffSiteInventoryBanner": "false",
        "showPhotosViewer": "false",
        "offsetSharedVehicleImageByOne": "false",
        "certifiedLogoColor": "",
        "certifiedDefaultPath": "",
        "certifiedDefaultLogoOnly": "false",
        "transferBadgeImage": "",
        "transferBadgeType": "DARK",
        "transferLinkHref": "",
        "certifiedBadgeLinkHref": "",
        "certifiedBadgeTooltip": "",
        "certifiedBadgeLinkTarget": "_self",
        "inTransitStatuses": "",
        "customInTransitLogoUrl": "",
        "carfaxLogoBlackWhite": "false",
        "hideCertifiedDefaultLogo": "false",
        "sorts": "year,normalBodyStyle,normalExteriorColor,odometer,internetPrice",
        "sortsTitles": "YEAR,BODYSTYLE,COLOR,MILEAGE,PRICE",
        "inventoryDateFormat": "MM_DD_YYYY_FORMAT",
        "offsiteInventoryMarkup": "0",
        "geoLocationEnhanced": "false",
        "showLocationTab": "true",
        "showEffectiveStartDate": "true",
        "showIncentiveTitleSubText": "true",
        "showIncentiveAmountAndLabel": "true",
        "showIncentiveDisclaimer": "true",
        "showIncentiveEffectiveDates": "true",
        "newCarBoostEnable": "false",
        "newCarBoostListingConfigId": "auto-new",
        "numberOfSpotlightVehicles": "3",
        "disableGeodistSort": "false",
        "required.tracking.attributes": ""
    },
    "includePricing": True,
    "flags": {
        "vcda-js-environment": "live",
        "ws-scripts-concurrency-limits-concurrency": 16,
        "ws-scripts-concurrency-limits-queue": 16,
        "ws-scripts-concurrency-limits-enabled": True,
        "ws-itemlist-service-version": "v5",
        "ws-itemlist-model-version": "v1",
        "ws-scripts-inline-css": True,
        "ws-inv-data-fetch-timeout": 5000,
        "ws-inv-data-fetch-retries": 2,
        "ws-inv-data-use-wis": True,
        "ws-inv-data-wis-fetch-timeout": 5000,
        "srp-track-fetch-resource-timing": False,
        "srp-test-package-data": 0,
        "ws-inv-data-preload-inventory": True,
        "ws-inv-data-location-service-fetch-timeout": 3000,
        "ws-inv-data-location-service-fetch-retries": 2,
        "wsm-account-data-distributor-timeout": 50,
        "wsm-account-data-distributor-retries": 2,
        "enable-client-side-geolocation-ws-inv-data": False,
        "ws-inv-data-spellcheck-proxy-timeout": 5000,
        "ws-inv-data-spellcheck-server-timeout": 1500,
        "ws-inv-data-spellcheck-server-retries": 0,
        "srp-toggle-databus-editor": True,
        "srp-send-ws-inv-data-prefs-to-wis": True,
        "ddc-ab-testing": "CONTROL"
    }
}

print("Starting crawl...")
all_vehicles = []
offset = 0
page_size = 18

while True:
    print(f"Fetching cars from offset={offset}...")
    payload = json.loads(json.dumps(base_payload))  # Deep copy
    if offset > 0:
        payload["inventoryParameters"]["start"] = [str(offset)]

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"Request failed at offset {offset}. Status: {response.status_code}")
        break

    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Failed to parse JSON.")
        break

    vehicles = data.get("inventory", [])
    if not vehicles:
        print("No more vehicles found. Done.")
        break

    all_vehicles.extend(vehicles)
    offset += page_size
    time.sleep(1)

# Save in chunks of 5000
chunk_size = 5000
for i in range(0, len(all_vehicles), chunk_size):
    chunk = all_vehicles[i:i + chunk_size]
    filename = f"autonation_inventory_part_{i // chunk_size + 1}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(chunk, f, indent=2)
    print(f"Saved {len(chunk)} vehicles to {filename}")

print(f"Done. Total vehicles saved: {len(all_vehicles)}")
