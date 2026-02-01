from .extensions import db
from datetime import datetime
import enum
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
import uuid

# --- Enums ---
class OrderStatus(str, enum.Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    PREPARING = 'preparing'
    READY = 'ready'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class PaymentStatus(str, enum.Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'
    REFUNDED = 'refunded'

class Role(str, enum.Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    KITCHEN = 'kitchen'
    CUSTOMER = 'customer'
    KIOSK = 'kiosk'

# --- Core/Tenancy ---
class Branch(db.Model):
    __tablename__ = 'branches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    settings = db.Column(db.JSON, default={}) # Store taxes, open hours, etc.
    users = db.relationship('User', backref='branch', lazy=True)
    orders = db.relationship('Order', backref='branch', lazy=True)
    devices = db.relationship('Device', backref='branch', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(Role), default=Role.CUSTOMER)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=True) # Staff belongs to branch
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Device(db.Model):
    """Kiosks, KDS screens, POS terminals"""
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(100), unique=True, nullable=False) # Hardware ID
    name = db.Column(db.String(100))
    type = db.Column(db.String(20)) # 'kiosk', 'kds', 'pos'
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    last_ping = db.Column(db.DateTime, default=datetime.utcnow)

# --- Menu ---
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    image_url = db.Column(db.String(255))
    display_order = db.Column(db.Integer, default=0)
    items = db.relationship('MenuItem', backref='category', lazy=True)

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False) # Base price
    image_url = db.Column(db.String(255))
    calories = db.Column(db.Integer)
    # Enterprise Visuals & Details
    allergens = db.Column(db.JSON, default=[]) # e.g. ['Gluten', 'Dairy']
    tags = db.Column(db.JSON, default=[]) # e.g. ['Spicy', 'Vegan', 'New']
    media = db.Column(db.JSON, default=[]) # e.g. [{'type': 'video', 'url': '...'}, {'type': 'image', 'url': '...'}]
    
    is_available = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # Relationships
    modifier_groups = db.relationship('ModifierGroup', secondary='menu_item_modifiers', backref='menu_items')

class ModifierGroup(db.Model):
    """e.g., 'Size', 'Toppings', 'Sauces'"""
    __tablename__ = 'modifier_groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    min_selection = db.Column(db.Integer, default=0)
    max_selection = db.Column(db.Integer, default=1)
    modifiers = db.relationship('Modifier', backref='group', lazy=True)

class Modifier(db.Model):
    """e.g., 'Small', 'Medium', 'Extra Cheese'"""
    __tablename__ = 'modifiers'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('modifier_groups.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    price_adjustment = db.Column(db.Numeric(10, 2), default=0.00)
    calories = db.Column(db.Integer, default=0)
    is_available = db.Column(db.Boolean, default=True)

# Join table for Items <-> Modifier Groups
menu_item_modifiers = db.Table('menu_item_modifiers',
    db.Column('menu_item_id', db.Integer, db.ForeignKey('menu_items.id'), primary_key=True),
    db.Column('modifier_group_id', db.Integer, db.ForeignKey('modifier_groups.id'), primary_key=True)
)

# --- Ordering ---
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True) # Daily short code e.g. #101
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=True) # Should be non-nullable in prod
    table_number = db.Column(db.Integer, nullable=True) # For eat-in orders
    
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    type = db.Column(db.String(20), default='eat_in') # eat_in, takeaway, delivery
    
    total_amount = db.Column(db.Numeric(10, 2), default=0.00)
    tax_amount = db.Column(db.Numeric(10, 2), default=0.00)
    estimated_prep_time = db.Column(db.Integer, default=0) # Minutes
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy=True)
    payments = db.relationship('Payment', backref='order', lazy=True)

    def transition_to(self, new_status):
        """
        Validates and transitions order status.
        Raises ValueError if transition is invalid.
        """

        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.PREPARING, OrderStatus.READY, OrderStatus.CANCELLED],
            OrderStatus.CONFIRMED: [OrderStatus.PREPARING, OrderStatus.READY, OrderStatus.CANCELLED],
            OrderStatus.PREPARING: [OrderStatus.READY, OrderStatus.CANCELLED], # Kitchen might cancel?

            OrderStatus.READY: [OrderStatus.COMPLETED],
            OrderStatus.COMPLETED: [], # Terminal
            OrderStatus.CANCELLED: []  # Terminal
        }

        if new_status not in valid_transitions.get(self.status, []):
            # Allow skipping steps for Admin/Manager override?
            # For now, strict.
            raise ValueError(f"Invalid transition from {self.status.value} to {new_status.value}")
        
        self.status = new_status
        self.updated_at = datetime.utcnow()
        db.session.commit()


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    menu_item_name = db.Column(db.String(100)) # Snapshot
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False) # Snapshot
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Store selected modifiers as JSON snapshot to simplify complexity
    # Structure: [{"name": "Extra Cheese", "price": 0.50, "group": "Toppings"}]
    modifiers_snapshot = db.Column(db.JSON, default=[])

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    method = db.Column(db.String(20)) # card, cash, kiosk_card
    status = db.Column(db.Enum(PaymentStatus), default=PaymentStatus.PENDING)
    transaction_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
