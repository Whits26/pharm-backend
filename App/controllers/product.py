from flask import Flask, redirect, jsonify, render_template, request, session, url_for

from App.models import Product
from App.models.database import db
from App import parse

from App.models import order

# COMMENTED OUT THIS CODE BECAUSE THERE IS NOW CODE TO CREATE A PRODUCT

#creates a new product for /create-product endpoint
#def create_product(code, name, category, supplier_price, supplier, qoh, stock, unit_price, total, image = None):
    #newProd = Product(code = code, product_name = name, category = category, supplier_cost_price = supplier_price, supplier = supplier, QoH = qoh, stock_unit = stock, unit_retail_price = unit_price, total_retail_price = total)
    #db.session.add(newProd)
    #db.session.commit()
    #print("Successfully added")
    #return newProd

# CREATE A NEW PRODUCT 
def productInput():
        post_data = request.get_json()

        code = post_data.get('code')
        product_name = post_data.get('product_name')
        category = post_data.get('category')
        supplier_cost_price = post_data.get('supplier_cost_price')
        supplier = post_data.get('supplier')
        QoH = post_data.get('QoH')
        stock_unit = post_data.get('stock_unit')
        unit_retail_price = post_data.get('unit_retail_price')
        total_retail_price = post_data.get('total_retail_price')
        image = post_data.get('image')

        reg = Product(code, product_name, category, supplier_cost_price, supplier, QoH, stock_unit, unit_retail_price, total_retail_price, image)

        db.session.add(reg)
        db.session.commit()

# GET ALL PRODUCTS 
def productAll():
        all_products = db.session.query(Product.id,
                                        Product.code, 
                                        Product.product_name, 
                                        Product.category, 
                                        Product.supplier_cost_price, 
                                        Product.supplier, 
                                        Product.QoH, 
                                        Product.stock_unit, 
                                        Product.unit_retail_price, 
                                        Product.total_retail_price, 
                                        Product.image).all()
        return all_products
    
# GET 1 PRODUCT FROM ALL
def productSingle(id):
    single_product = db.session.query(Product.id,
                                      Product.code, 
                                      Product.product_name, 
                                      Product.category, 
                                      Product.supplier_cost_price, 
                                      Product.supplier, 
                                      Product.QoH, 
                                      Product.stock_unit, 
                                      Product.unit_retail_price, 
                                      Product.total_retail_price, 
                                      Product.image).filter(Product.id == id).first()
    return single_product

# UPDATE EACH PRODUCT RECORD BY ID
def productUpdate(id):
        put_data = request.get_json()

        code = put_data.get('code')
        product_name = put_data.get('product_name')
        category = put_data.get('category')
        supplier_cost_price = put_data.get('supplier_cost_price')
        supplier = put_data.get('supplier')
        QoH = put_data.get('QoH')
        stock_unit = put_data.get('stock_unit')
        unit_retail_price = put_data.get('unit_retail_price')
        total_retail_price = put_data.get('total_retail_price')
        image = put_data.get('image')

        record = db.session.query(Product).get(id)

        record.code = code
        record.product_name = product_name
        record.category = category
        record.supplier_cost_price = supplier_cost_price
        record.supplier = supplier
        record.QoH = QoH
        record.stock_unit = stock_unit
        record.unit_retail_price = unit_retail_price
        record.total_retail_price = total_retail_price
        record.image = image

        db.session.commit()
        


# DELETE PRODUCT BY ID
def productDelete(id):
    record = db.session.query(Product).get(id)
    db.session.delete(record)
    db.session.commit()
    return 'Deleted'

# calls the parse.py view method to parse the given excel products file
def parse_excel():
    print('Product controller parse excel')
    prodList = parse.parse()

    print('Inserting products in DB (This may take several minutes).....')
    if prodList:
        for p in prodList:
            #print('Code: {}\nProduct Name: {}\nCategory: {}\nSupplier Cost Price: {}\nSupplier: {}\nQoH: {}\nStock Unit: {}\nUnit Retail: {}\nTotal Retail Price: {}\n'
            #.format(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]))

            x = create_product(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8])
        print('Finished!')
        return 1
    else:
        print('No products parsed')
        return 0


# gets 20 products (pagination) per page
ROWS_PER_PAGE = 20
def get_products_page(page):
    print('getting 20 products')
    list_of_products = []
    page = request.args.get('page', page, type=int)
    query = Product.query.paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)
    products = query.items
    if products:
        list_of_products = [product.toDict() for product in products]
    return list_of_products

# wasn't in use yet - made in case you'd want to get numbers instead of
# previous and next buttons for pagination
def get_page_details(page):
    page = request.args.get('page', page, type=int)
    query = Product.query.paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)
    #total_products = query.total
    total_pages = query.pages
    has_next = query.has_next
    has_prev = query.has_prev
    page_details = [{
        "total_pages" : total_pages,
        "has_prev" : has_prev,
        "has_next" : has_next,
    }]
    return page_details

# gets a list of distinct categories from the products
def get_product_categories():
    query = Product.query.with_entities(Product.category).distinct()
    titles = [row.category for row in query.all()]
    return titles

# get all products from DB
def get_products():
    print('get_products')
    products = Product.query.all()
    list_of_products = []
    if products:
        list_of_products = [p.toDict() for p in products]
    return list_of_products

# delete all products from DB
def delete_products():
    print('delete_products')
    x = Product.query.delete()
    db.session.commit()
    print('Rows deleted: ',x)
    return 0


#search through products; used in /search endpoint
def get_products_by_term(term):
    list_of_products = []
    products = Product.query.filter(
        Product.product_name.contains(term) 
        | Product.category.contains(term) 
        | Product.code.contains(term) 
        | Product.supplier.contains(term)
    )
    if products:
        list_of_products = [p.toDict() for p in products]
    return list_of_products

# get a particular product by its URL-Friendly slug
def get_product_by_slug(p_slug):
    print("getting product")
    p_name = p_slug.upper().replace('-', ' ')
    product = Product.query.filter(Product.product_name == p_name).first() # if this returns a user, then the email already exists in database
    return product

# delete a particular product by its URL-Friendly slug
def delete_product_by_slug(p_slug):
    print("deleting product")
    p_name = p_slug.upper().replace('-', ' ')
    product = Product.query.filter(Product.product_name == p_name).first() # if this returns a user, then the email already exists in database
    if product:
        if product.orders:
            return False

        db.session.delete(product)
        db.session.commit()
        return True
    return False

