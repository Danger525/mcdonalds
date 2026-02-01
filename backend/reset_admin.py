
from app import create_app, db
from app.models import User, Role

app = create_app('development')

def reset():
    with app.app_context():
        print("Resetting Admin Password...")
        db.create_all() # Ensure tables exist
        
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("Admin not found. Creating...")
            user = User(username='admin', email='admin@hq.com', role=Role.ADMIN)
            db.session.add(user)
        else:
            print("Admin found. Updating password...")
            
        user.set_password('admin123')
        db.session.commit()
        print("Done. Login with admin / admin123")

if __name__ == "__main__":
    reset()
