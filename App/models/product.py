from .database import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, unique=True, nullable=False)
    product_name = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(300), nullable=False)     
    supplier_cost_price = db.Column(db.Float(decimal_return_scale=2), nullable=False)
    supplier = db.Column(db.String(200), nullable = False)    
    QoH = db.Column(db.Integer, nullable = False)
    stock_unit = db.Column(db.Integer, nullable = False)
    unit_retail_price = db.Column(db.Float(decimal_return_scale=2), nullable = False)
    total_retail_price = db.Column(db.Float(decimal_return_scale=2), nullable=False)
    image = db.Column(db.String(300), nullable=True)
    orders = db.relationship("ProductOrder", back_populates="product")

    def __init__(self, code, product_name, category, supplier_cost_price, supplier, QoH, stock_unit, unit_retail_price, total_retail_price, image):
        self.code = code
        self.product_name = product_name
        self.category = category
        self.supplier_cost_price = supplier_cost_price
        self.supplier = supplier   
        self.QoH = QoH
        self.stock_unit = stock_unit
        self.unit_retail_price = unit_retail_price
        self.total_retail_price = total_retail_price
        self.image = image

    def __repr__(self):
        return f"{self.code}"



    def setPrice(self, price):
        self.unit_retail_price = price

    def toDict(self):
        return {
            "code": self.code,
            "product_name": self.product_name,
            "category": self.category,
            "supplier": self.supplier,
            "supplier_cost_price": round(self.supplier_cost_price,2),
            "QoH": self.QoH,
            "stock_unit": self.stock_unit,
            "unit_retail_price": round(self.unit_retail_price,2),
            "total_retail_price": round(self.total_retail_price,2),
            "image" : self.image,
            "slug" : self.product_name.lower().replace(' ', '-')
            # uncomment for all orders containing the product "orders": [OrderProduct.order.toDict() for OrderProduct in self.orders]
        }
