import requests

BASE_URL = "http://localhost:5000/api/cart"

def verify_cart():
    print("Testing Redis Cart...")
    headers = {"X-Session-ID": "test-session-123"}
    
    # 1. Clear Cart
    requests.delete(f"{BASE_URL}/", headers=headers)
    
    # 2. Add Item
    resp = requests.post(f"{BASE_URL}/items", headers=headers, json={"menu_item_id": 1, "quantity": 2})
    if resp.status_code == 200:
        print(f"  Added item: {resp.json()}")
    else:
        print(f"  Failed add: {resp.text}")
        
    # 3. Get Cart
    resp = requests.get(f"{BASE_URL}/", headers=headers)
    data = resp.json()
    if len(data['items']) == 1 and data['items'][0]['qty'] == 2:
        print("  [Pass] Cart Persistence Verified")
    else:
        print(f"  [Fail] Cart Data Mismatch: {data}")

if __name__ == "__main__":
    verify_cart()
