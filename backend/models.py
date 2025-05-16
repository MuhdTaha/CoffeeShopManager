from app import db

class Employee(db.Model):
    __tablename__ = 'employees'
    ssn = db.Column(db.String(9), primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    salary = db.Column(db.Numeric(10, 2), nullable=False)

    manager = db.relationship("Manager", backref="employee", uselist=False)
    barista = db.relationship("Barista", backref="employee", uselist=False)


class Manager(db.Model):
    __tablename__ = 'managers'
    ssn = db.Column(db.String(9), db.ForeignKey('employees.ssn'), primary_key=True)
    ownership_percentage = db.Column(db.Numeric(5, 2), nullable=False)


class Barista(db.Model):
    __tablename__ = 'baristas'
    ssn = db.Column(db.String(9), db.ForeignKey('employees.ssn'), primary_key=True)

    schedules = db.relationship("Schedule", backref="barista")


class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.String(9), db.ForeignKey('baristas.ssn'))
    day_of_week = db.Column(db.String, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)


class Accounting(db.Model):
    __tablename__ = 'accounting'
    time_stamp = db.Column(db.DateTime, primary_key=True)
    balance = db.Column(db.Numeric(12, 2), nullable=False)


class Menu(db.Model):
    __tablename__ = 'menu'
    name = db.Column(db.Text, primary_key=True)
    size = db.Column(db.Numeric(5, 2), nullable=False)
    type = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric(6, 2), nullable=False)
    temperature = db.Column(db.String, nullable=False)

    recipe = db.relationship("Recipe", backref="menu", uselist=False)
    lineitems = db.relationship("LineItem", backref="menu")
    promo_items = db.relationship("PromotionItem", backref="menu")


class Recipe(db.Model):
    __tablename__ = 'recipe'
    recipe_id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.Text, db.ForeignKey('menu.name'), unique=True)

    ingredients = db.relationship("Ingredient", backref="recipe")
    preparation_steps = db.relationship("PreparationStep", backref="recipe")


class PreparationStep(db.Model):
    __tablename__ = 'preparation_step'
    step_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'))
    position = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, nullable=False)


class Inventory(db.Model):
    __tablename__ = 'inventory'
    name = db.Column(db.Text, primary_key=True)
    unit = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(6, 2), nullable=False)
    quantity_in_stock = db.Column(db.Numeric(10, 2), nullable=False)

    ingredients = db.relationship("Ingredient", backref="inventory")


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    ingredient_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'))
    inventory_name = db.Column(db.Text, db.ForeignKey('inventory.name'))
    quantity = db.Column(db.Numeric(8, 3), nullable=False)
    unit = db.Column(db.Text, nullable=False)


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    time_stamp = db.Column(db.DateTime, nullable=False)
    payment_method = db.Column(db.String, nullable=False)

    lineitems = db.relationship("LineItem", backref="order")


class LineItem(db.Model):
    __tablename__ = 'lineitem'
    lineitem_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    menu_name = db.Column(db.Text, db.ForeignKey('menu.name'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(6, 2), nullable=False)


class Promotion(db.Model):
    __tablename__ = 'promotions'
    promotion_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    day_of_week = db.Column(db.String, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    items = db.relationship("PromotionItem", backref="promotion")


class PromotionItem(db.Model):
    __tablename__ = 'promotion_items'
    promotion_item_id = db.Column(db.Integer, primary_key=True)
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotions.promotion_id'))
    menu_name = db.Column(db.Text, db.ForeignKey('menu.name'))
    promo_price = db.Column(db.Numeric(6, 2), nullable=False)
