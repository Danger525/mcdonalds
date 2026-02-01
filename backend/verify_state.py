import requests
import sys

BASE_URL = "http://localhost:5000/api"

def verify_state():
    print("Testing State Machine...")
    
    # 1. Login as Admin/Manager to get token (needed for status updates)
    s = requests.Session()
    resp = s.post(f"{BASE_URL}/auth/login", json={"username": "admin", "password": "admin123"})
    if resp.status_code != 200:
        print("Login failed")
        return
    token = resp.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Create Order
    resp = s.post(f"{BASE_URL}/orders/", json={
        "items": [{"menu_item_id": 1, "quantity": 1}],
        "table_number": 5
    })
    order_id = resp.json()['order_id']
    print(f"Created Order {order_id} (PENDING)")
    
    # 3. Valid Transition: PENDING -> CONFIRMED
    resp = s.put(f"{BASE_URL}/orders/{order_id}/status", headers=headers, json={"status": "confirmed"})
    if resp.status_code == 200:
        print("  [Pass] PENDING -> CONFIRMED")
    else:
        print(f"  [Fail] PENDING -> CONFIRMED: {resp.text}")

    # 4. Invalid Transition: CONFIRMED -> COMPLETED (Skip PREPARING/READY)
    resp = s.put(f"{BASE_URL}/orders/{order_id}/status", headers=headers, json={"status": "completed"})
    if resp.status_code == 400:
        print("  [Pass] Blocked Invalid Transition (CONFIRMED -> COMPLETED)")
    else:
        print(f"  [Fail] Allowed Invalid Transition: {resp.status_code}")

if __name__ == "__main__":
    verify_state()
