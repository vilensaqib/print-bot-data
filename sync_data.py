import os
import json
from woocommerce import API

# Setup WooCommerce API
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
        # Fetching 100 products at a time
        r = wcapi.get("products", params={"per_page": 100, "page": page}).json()
        if not r: break
        
        for p in r:
            # Sirf Variable products uthao kyunki printing mein variations hi hoti hain
            if p['type'] == 'variable':
                variations = wcapi.get(f"products/{p['id']}/variations").json()
                var_list = []
                for v in variations:
                    var_list.append({
                        "attributes": v['attributes'],
                        "price": v['display_regular_price'] if 'display_regular_price' in v else v['price'],
                        "url": p['permalink']
                    })
                
                products.append({
                    "name": p['name'],
                    "id": p['id'],
                    "variations": var_list
                })
        page += 1
    
    with open("catalog.json", "w") as f:
        json.dump(products, f, indent=2)

if __name__ == "__main__":
    fetch_products()
