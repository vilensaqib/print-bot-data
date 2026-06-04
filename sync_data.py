import os
import json
from woocommerce import API

wcapi = API(
    url=os.environ.get("WC_URL"),
    consumer_key=os.environ.get("WC_KEY"),
    consumer_secret=os.environ.get("WC_SECRET"),
    version="wc/v3",
    timeout=30
)

# sync_data.py ke andar modification:
def fetch_products():
    products = []
    page = 1
    while True:
        print(f"Fetching page {page}...")
        response = wcapi.get("products", params={"per_page": 100, "page": page, "status": "publish"})
        
        # Check for API errors safely
        if response.status_code != 200:
            print(f"API Error on page {page}: {response.text}")
            break
            
        r = response.json()
        if not r or 'message' in r or len(r) == 0: 
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
    
    # Isse pehle ka baki saara code bilkul same rahega...

    print(f"Total products fetched: {len(products)}")
    with open("catalog.json", "w") as f:
        json.dump(products, f, indent=2)
    print("catalog.json successfully written.")

# Seedhe function call karein (if __name__ hatakar)
fetch_products()
