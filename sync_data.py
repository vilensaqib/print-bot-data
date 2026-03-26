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

def fetch_products():
    products = []
    page = 1
    while True:
        r = wcapi.get("products", params={"per_page": 100, "page": page, "status": "publish"}).json()
        if not r or 'message' in r: break
        
        for p in r:
            # Extracting Add-ons from Meta Data
            addons = []
            meta = p.get('meta_data', [])
            for m in meta:
                if m.get('key') == '_product_addons':
                    addons = m.get('value', [])
            
            products.append({
                "name": p['name'],
                "id": p['id'],
                "base_price": p.get('price') or "0",
                "addons": addons, # This contains Quantity, Side, Lamination etc.
                "url": p['permalink']
            })
        page += 1
    
    with open("catalog.json", "w") as f:
        json.dump(products, f, indent=2)

if __name__ == "__main__":
    fetch_products()
