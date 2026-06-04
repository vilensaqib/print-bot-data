import os
import json
from woocommerce import API

# Nayi keys direct code mein inject kar di hain testing ke liye
URL = "https://printeldeziner.com"
KEY = "ck_a15c85fd40eb0e6209e55a0dde853daebd136376"
SECRET = "cs_370fcb99788dd6c659bc654cb29fd6d085368394"

print(f"Connecting to WooCommerce API at: {URL}")

wcapi = API(
    url=URL,
    consumer_key=KEY,
    consumer_secret=SECRET,
    version="wc/v3",
    timeout=30
)

def fetch_products():
    products = []
    page = 1
    
    while True:
        print(f"Fetching page {page}...")
        response = wcapi.get("products", params={"per_page": 100, "page": page, "status": "publish"})
        print(f"Page {page} Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"API Error: {response.text}")
            break
            
        r = response.json()
        if not r or len(r) == 0: 
            break
        
        print(f"Found {len(r)} products on page {page}.")
        for p in r:
            addons = []
            meta = p.get('meta_data', [])
            for m in meta:
                if m.get('key') == '_product_addons':
                    addons = m.get('value', [])
            
            products.append({
                "name": p['name'],
                "id": p['id'],
                "base_price": p.get('price') or "0",
                "addons": addons,
                "url": p['permalink']
            })
        page += 1
    
    print(f"Total products successfully parsed: {len(products)}")
    
    with open("catalog.json", "w") as f:
        json.dump(products, f, indent=2)
    print("catalog.json successfully written.")

fetch_products()
