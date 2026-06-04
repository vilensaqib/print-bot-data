import os
import json
import sys
from woocommerce import API

# Get URL safely and remove any trailing slash if present, then add a clean one
raw_url = os.environ.get("WC_URL", "").strip()
if raw_url.endswith("/"):
    raw_url = raw_url[:-1]

print(f"Connecting to WooCommerce API at: {raw_url}")

try:
    wcapi = API(
        url=raw_url,
        consumer_key=os.environ.get("WC_KEY"),
        consumer_secret=os.environ.get("WC_SECRET"),
        version="wc/v3",
        timeout=30
    )
except Exception as e:
    print(f"Initialization Error: {e}")
    sys.exit(1)

def fetch_products():
    products = []
    page = 1
    
    while True:
        print(f"Fetching page {page}...")
        try:
            response = wcapi.get("products", params={"per_page": 100, "page": page, "status": "publish"})
            
            # Print response status for debugging
            print(f"Page {page} Status Code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"API Error on page {page}: {response.text}")
                break
                
            r = response.json()
            if not r or 'message' in r or len(r) == 0: 
                print(f"No more products or end of pages reached at page {page}.")
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
            
        except Exception as err:
            print(f"Network or request crash on page {page}: {err}")
            break
    
    print(f"Total products successfully parsed: {len(products)}")
    
    # Check if we actually got products before overwriting with an empty list
    if len(products) == 0:
        print("WARNING: 0 products fetched. Not writing catalog.json to prevent breaking the blog.")
        return

    with open("catalog.json", "w") as f:
        json.dump(products, f, indent=2)
    print("catalog.json successfully written and updated.")

# Function call direct executing
fetch_products()
