from app import create_app, db
from app.models import MenuItem

app = create_app('development')

def verify():
    with app.app_context():
        items = MenuItem.query.filter(MenuItem.allergens != None).all()
        for item in items:
            print(f"Item: {item.name}")
            print(f"  Allergens: {item.allergens}")
            print(f"  Media: {item.media}")
            print("-" * 20)

if __name__ == "__main__":
    verify()
