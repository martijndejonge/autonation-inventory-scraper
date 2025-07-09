import requests
import json
import csv
import time
import re
import os

HEADERS_TEMPLATE = {
    "accept": "*/*",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

BASE_PAYLOAD = {
    "siteId": "",  # to be filled in
    "locale": "en_US",
    "device": "DESKTOP",
    "pageAlias": "INVENTORY_LISTING_DEFAULT_AUTO_NEW",
    "pageId": "",  # to be filled in
    "windowId": "inventory-data-bus2",
    "widgetName": "ws-inv-data",
    "inventoryParameters": {},
    "preferences": {
        "pageSize": "18",
        "listing.config.id": "auto-new",
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
        "suppressAllConditions": "compliant",
        "violateUsedCompliance": "false",
        "showOffSiteInventoryBanner": "false",
        "showPhotosViewer": "false",
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
        "disableGeodistSort": "false"
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

def extract_site_id(inventory_url):
    try:
        response = requests.get(inventory_url, timeout=10)
        if response.status_code != 200:
            return None
        match = re.search(r'"siteId"\s*:\s*"([a-zA-Z0-9]+)"', response.text)
        return match.group(1) if match else None
    except Exception:
        return None

def scrape_inventory(dealer_name, site_url, site_id):
    safe_name = dealer_name.lower().replace(" ", "_").replace("/", "_")
    inventory_url = f"{site_url.rstrip('/')}/api/widget/ws-inv-data/getInventory"
    referer_url = f"{site_url.rstrip('/')}/new-inventory/index.htm"
    
    headers = HEADERS_TEMPLATE.copy()
    headers["referer"] = referer_url
    headers["origin"] = site_url.rstrip('/')

    payload = json.loads(json.dumps(BASE_PAYLOAD))  # deep copy
    payload["siteId"] = site_id
    payload["pageId"] = f"{site_id}_SITEBUILDER_INVENTORY_SEARCH_RESULTS_AUTO_NEW_V1_1"

    all_vehicles = []
    offset = 0
    page_size = 18

    while True:
        if offset > 0:
            payload["inventoryParameters"]["start"] = [str(offset)]

        try:
            res = requests.post(inventory_url, headers=headers, json=payload, timeout=15)
            if res.status_code != 200:
                print(f"Error {res.status_code} at offset {offset} for {dealer_name}")
                break
            data = res.json()
        except Exception as e:
            print(f"Failed to fetch inventory for {dealer_name}: {e}")
            break

        vehicles = data.get("inventory", [])
        if not vehicles:
            break

        all_vehicles.extend(vehicles)
        offset += page_size
        time.sleep(1)

    if all_vehicles:
        os.makedirs("output", exist_ok=True)
        with open(f"output/{safe_name}_inventory.json", "w", encoding="utf-8") as f:
            json.dump(all_vehicles, f, indent=2)
        print(f"Saved {len(all_vehicles)} vehicles for {dealer_name}")
    else:
        print(f"No vehicles found for {dealer_name}")

def main():
    with open("dealers.csv", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        dealers = list(reader)

    for dealer in dealers:
        name = dealer["Dealer Name"]
        url = dealer["URL"]
        inventory_page = url.rstrip("/") + "/new-inventory/index.htm"

        print(f"\nProcessing {name}...")

        site_id = extract_site_id(inventory_page)
        if not site_id:
            print(f"❌ Failed to extract siteId for {name}")
            continue

        scrape_inventory(name, url, site_id)

if __name__ == "__main__":
    main()
