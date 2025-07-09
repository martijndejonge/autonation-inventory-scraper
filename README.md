# AutoNation Dealership Inventory Scraper

This Python project scrapes **new and used vehicle inventory data** from over 250 AutoNation dealership websites. 
It extracts full listings from each dealer’s `/all-inventory` page using dynamic API calls, parses the JSON payload, and stores the results as `.json` files per dealer — with automatic chunking for large datasets.

---

## 🚗 Features

- Scrapes inventory for **all vehicle types** (new, used, CPO).
- Extracts the required `siteId` dynamically per dealership.
- Follows AutoNation’s internal API structure for accurate, fast scraping.
- Handles timeouts, retries, and pagination.
- Automatically splits large files into **chunks of 1000 vehicles**.
- Saves output to `/output/` folder as prettified JSON files.

---

## 📄 dealers.csv Format

CSV file with headers:

Dealer Name,Store ID,URL

Audi Westmont,2831,https://www.audiwestmont.com/

Laurel BMW of Westmont,2832,https://www.laurelbmw.com/
...


🚀 How to Run
Install dependencies (Python 3.7+ recommended):

pip install requests

Place your dealers.csv in the root folder.

Run the scraper:
- autonation_all_scraper_sites.py (all cars, new and used)
- autonation_new_scraper_sites.py (only new cars)

Check output/ folder for JSON files:

Example: output/audi_westmont_all_inventory.json

If vehicle count >1000:
output/laurel_bmw_of_westmont_all_inventory_part1.json, part2.json, etc.

🛠 Configuration
Main configuration is inside autonation_all_scraper_sites.py, including:

Payload structure (BASE_PAYLOAD)
Headers (HEADERS_TEMPLATE)
Pagination control (pageSize)

Chunking logic (if len(all_vehicles) > 1000)



⚠️ Notes
This project is for educational/research purposes.

Use responsibly and in accordance with AutoNation's terms of service.

The API is undocumented and may change or restrict access in the future.
