from app import create_app, db
from app.models import User, Category, MenuItem, Branch, ModifierGroup, Modifier, Role

app = create_app('development')

def seed():
    with app.app_context():
        print("Seeding Enterprise Menu System with Rich Data...")
        db.create_all()


        # 1. Create Main Branch
        main_branch = Branch.query.filter_by(name="Mumbai Flagship").first()
        if not main_branch:
            main_branch = Branch(name="Mumbai Flagship", location="Linking Road, Bandra", settings={"tax_rate": 0.05, "currency": "INR"})
            db.session.add(main_branch)
            db.session.commit()

        # 2. Create Users
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@mcdindia.com', role=Role.ADMIN, branch_id=main_branch.id)
            admin.set_password('admin123')
            db.session.add(admin)

        if not User.query.filter_by(username='kitchen01').first():
            kitchen = User(username='kitchen01', role=Role.KITCHEN, branch_id=main_branch.id)
            kitchen.set_password('kitchen123')
            db.session.add(kitchen)
            
        db.session.commit()

        # 3. Modifiers
        size_group = ModifierGroup.query.filter_by(name="Size").first()
        if not size_group:
            size_group = ModifierGroup(name="Size", min_selection=1, max_selection=1)
            db.session.add(size_group)
            db.session.add(Modifier(group=size_group, name="Regular", price_adjustment=0))
            db.session.add(Modifier(group=size_group, name="Medium", price_adjustment=60.00))
            db.session.add(Modifier(group=size_group, name="Large", price_adjustment=90.00))
            db.session.commit()


        # 5. McDonald's India Menu Items
        items_data = [
            # BURGERS (Veg)
            {
                "name": "McAloo Tikki Burger", 
                "price": 60.00, 
                "cat": "Burgers", 
                "allergens": ["Gluten", "Soy"],
                "tags": ["Bestseller", "Veg", "Classic"],
                "media": [{"type": "image", "url": "https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?auto=format&fit=crop&w=500&q=60"}]
            },
            {
                "name": "McVeggie Burger", 
                "price": 129.00, 
                "cat": "Burgers", 
                "allergens": ["Gluten", "Dairy", "Soy"],
                "tags": ["Veg", "Crispy"],
                "media": [{"type": "image", "url": "https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=500&q=60"}]
            },
            {
                "name": "McSpicy Paneer Burger", 
                "price": 179.00, 
                "cat": "Burgers", 
                "allergens": ["Gluten", "Dairy", "Soy"],
                "tags": ["Veg", "Spicy", "Premium"],
                "media": [{"type": "image", "url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=500&q=60"}]
            },
            {
                "name": "Veg Maharaja Mac", 
                "price": 229.00, 
                "cat": "Burgers", 
                "allergens": ["Gluten", "Dairy"],
                "tags": ["Veg", "Double Patty", "Big"],
                "media": [{"type": "image", "url": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?auto=format&fit=crop&w=500&q=60"}]
            },
            
            # BURGERS (Non-Veg)
            {
                "name": "McChicken Burger", 
                "price": 135.00, 
                "cat": "Burgers", 
                "allergens": ["Gluten", "Poultry"],
                "tags": ["Non-Veg", "Classic"],
                "media": [{"type": "image", "url": "https://images.unsplash.com/photo-1615297371902-86aac374737f?auto=format&fit=crop&w=500&q=60"}]
            },
            {
                "name": "McSpicy Chicken Burger", 
                "price": 185.00, 
                "cat": "Burgers", 
                "allergens": ["Gluten", "Poultry", "Soy"],
                "tags": ["Non-Veg", "Spicy"],
                "media": [{"type": "image", "url": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=500&q=60"}]
            },
             {
                "name": "Filet-O-Fish Burger", 
                "price": 169.00, 
                "cat": "Burgers", 
                "allergens": ["Gluten", "Fish", "Dairy"],
                "tags": ["Non-Veg", "Seafood"],
                "media": [{"type": "image", "url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=500&q=60"}]
            },
            {
                "name": "Chicken Maharaja Mac", 
                "price": 249.00, 
                "cat": "Burgers", 
                "allergens": ["Gluten", "Poultry", "Dairy"],
                "tags": ["Non-Veg", "Big", "Premium"],
                "media": [{"type": "image", "url": "https://images.unsplash.com/photo-1625813506062-0aeb1d7a0956?auto=format&fit=crop&w=500&q=60"}]
            },

            # SIDES
            {
                "name": "Fries (Regular)", 
                "price": 75.00, 
                "cat": "Sides", 
                "allergens": [],
                "tags": ["Veg", "Classic"],
                "media": [{"type": "image", "url": "https://images.unsplash.com/photo-1630384060421-a4323ceca0ad?auto=format&fit=crop&w=500&q=60"}]
            },
            {
                "name": "Pizza McPuff", 
                "price": 49.00, 
                "cat": "Sides", 
                "allergens": ["Gluten", "Dairy"],
                "tags": ["Veg", "Hot"],
                "media": [{"type": "image", "url": "https://images.unsplash.com/photo-1626074353765-517a681e40be?auto=format&fit=crop&w=500&q=60"}]
            },
             {
                "name": "Chicken McNuggets (6 Pc)", 
                "price": 169.00, 
                "cat": "Sides", 
                "allergens": ["Gluten", "Poultry"],
                "tags": ["Non-Veg", "Shareable"],
                "media": [{"type": "image", "url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=500&q=60"}]
            },

            # DESSERTS
            {
                "name": "McFlurry Oreo", 
                "price": 99.00, 
                "cat": "Desserts", 
                "allergens": ["Dairy", "Gluten"],
                "tags": ["Veg", "Sweet", "Cold"],
                "media": [{"type": "image", "url": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?auto=format&fit=crop&w=500&q=60"}]
            },
            {
                "name": "Soft Serve Cone", 
                "price": 35.00, 
                "cat": "Desserts", 
                "allergens": ["Dairy"],
                "tags": ["Veg", "Sweet"],
                "media": [{"type": "image", "url": "https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?auto=format&fit=crop&w=500&q=60"}]
            },
            
             # BEVERAGES
            {
                "name": "Coca-Cola (Glass)", 
                "price": 60.00, 
                "cat": "Beverages", 
                "allergens": [],
                "tags": ["Veg", "Cold"],
                "media": [{"type": "image", "url": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=500&q=60"}]
            },
             {
                "name": "Cold Coffee", 
                "price": 89.00, 
                "cat": "Beverages", 
                "allergens": ["Dairy"],
                "tags": ["Veg", "Cold", "Caffeine"],
                "media": [{"type": "image", "url": "https://images.unsplash.com/photo-1517701604599-bb29b5c5090c?auto=format&fit=crop&w=500&q=60"}]
            }
        ]


        # Update categories list first
        cats_data = [
            ('Burgers', 'The classics'), 
            ('Sides', 'Crispy Add-ons'), 
            ('Desserts', 'Sweet Treats'), 
            ('Beverages', 'Thirst Quenchers')
        ]
        
        cat_objs = {}
        for c_name, c_desc in cats_data:
            cat = Category.query.filter_by(name=c_name).first()
            if not cat:
                cat = Category(name=c_name, description=c_desc)
                db.session.add(cat)
            cat_objs[c_name] = cat
        db.session.commit()
    

        for i in items_data:
            # Check by exact name match to avoid duplicates if re-seeding
            item = MenuItem.query.filter_by(name=i['name']).first()
            if not item:

                item = MenuItem(
                    name=i['name'],
                    price=i['price'],
                    category_id=cat_objs[i['cat']].id,
                    is_available=True,
                    allergens=i['allergens'],
                    tags=i['tags'],
                    media=i['media'],
                    image_url=i['media'][0]['url'] if i['media'] else None
                )

                item.modifier_groups.append(size_group)
                db.session.add(item)
                print(f"Added: {i['name']}")

            else:
                # Update price/data for existing
                item.price = i['price'] # Enforce price update
                item.allergens = i['allergens']
                item.tags = i['tags']
                item.media = i['media']
                if i['media']:
                    item.image_url = i['media'][0]['url']
                print(f"Updated: {i['name']}")


        db.session.commit()
        print("McDonald's India Menu Seeded Successfully!")


if __name__ == "__main__":
    seed()
