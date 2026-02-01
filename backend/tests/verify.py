import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def test_flow():
    session = requests.Session()
    
    print("1. Registering Admin...")
    reg_data = {"username": "admin", "password": "password", "role": "admin"}
    res = session.post(f"{BASE_URL}/api/auth/register", json=reg_data)
    print(res.status_code, res.json())
    
    print("\n2. Logging in...")
    login_data = {"username": "admin", "password": "password"}
    res = session.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if res.status_code != 200:
        print("Login failed")
        return
    token = res.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful, Token received.")

    print("\n3. Adding Menu Item...")
    item_data = {
        "name": "Burger", 
        "price": 10.99, 
        "category": "Main", 
        "description": "Tasty burger"
    }
    res = session.post(f"{BASE_URL}/api/menu/", json=item_data, headers=headers)
    print(res.status_code, res.json())
    item_id = res.json().get('message') == 'Menu item added' and 1 # Assuming ID is 1 if it's first

    print("\n4. Getting Menu...")
    res = session.get(f"{BASE_URL}/api/menu/")
    print(res.status_code, res.json())
    menu_items = res.json()
    if not menu_items:
        print("No items found!")
        return
    menu_item_id = menu_items[0]['id']

    print("\n5. Placing Order...")
    order_data = {
        "table_number": 5,
        "items": [{"menu_item_id": menu_item_id, "quantity": 2}]
    }
    res = session.post(f"{BASE_URL}/api/orders/", json=order_data)
    print(res.status_code, res.json())
    order_id = res.json().get('order_id')

    print(f"\n6. Checking Order {order_id} Status...")
    res = session.get(f"{BASE_URL}/api/orders/{order_id}")
    print(res.status_code, res.json())

    print("\n7. Updating Order Status (Admin)...")
    status_data = {"status": "ready"}
    res = session.put(f"{BASE_URL}/api/orders/{order_id}/status", json=status_data, headers=headers)
    print(res.status_code, res.json())

    print("\n8. Admin Stats...")
    res = session.get(f"{BASE_URL}/api/admin/stats", headers=headers)
    print(res.status_code, res.json())

if __name__ == "__main__":
    test_flow()
