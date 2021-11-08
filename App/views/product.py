from flask import Blueprint, request, jsonify, Flask
from flask_jwt import jwt_required

from App.models import Product
from App.models.database import db

from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename


product_views = Blueprint('product_views', __name__, template_folder='../templates')

from App.controllers import (
    get_products_page,
    get_page_details,
    get_product_categories,
    get_product_by_slug,
    delete_product_by_slug,
    productInput,
    productAll,
    productSingle,
    productDelete,
    productUpdate

)

#get 20 products based on page
@product_views.route('/products', methods=["GET"])
def display_event():
    page = request.args.get('page')
    prodList = get_products_page(page)
    return jsonify(prodList)

#display page details based on page # - not used - future proofing
@product_views.route('/products_page', methods=["GET"])
def display_pages():
    page = request.args.get('page')
    pageList = get_page_details(page)
    return jsonify(pageList)

# get product categories
@product_views.route('/product_categories', methods=["GET"])
def display_categories():
    categoryList = get_product_categories()
    return jsonify(categoryList)

# get product endpoint
@product_views.route('/product', methods=["GET"])
def get_product():
    product_slug = request.args.get("slug")
    product = get_product_by_slug(product_slug)
    if product is None:
        return jsonify({ 'message' :'product not found' }), 404
    return jsonify(product.toDict())

# COMMENTED OUT THIS CODE BECAUSE THERE IS NOW CODE TO CREATE A PRODUCT

# create product - wasn't fully implemented due to Firebase not setup
#@product_views.route('/create-product', methods=["POST"])
#@jwt_required()
#def create_product():
    #code = request.json.get("code")
    #name = request.json.get("name")
    #category = request.json.get("category")
    #supplier_cost_price = request.json.get("supplier_cost_price")
    #supplier = request.json.get("supplier")
    #QoH = request.json.get("QoH")
    #stock_unit = request.json.get("stock_unit")
    #unit_retail_price = request.json.get("unit_retail_price")
    #total_retail_price = request.json.get("total_retail_price")
    #image = request.json.get("image")

    # product = create_product(code, name, category, supplier_cost_price,supplier,QoH,stock_unit,unit_retail_price,total_retail_price, image )
    #return jsonify(product.toDict())

# delete product by slug
@product_views.route('/delete-product', methods=["DELETE"])
def delete_product():
    product_slug = request.args.get("slug")
    deleted = delete_product_by_slug(product_slug)
    return jsonify({"deleted": deleted})



# CREATE / POST A NEW PRODUCT
@product_views.route('/product/input', methods=['POST'])
@jwt_required()
def post_productInput():
    if request.content_type == 'application/json':
        try:
            EnterProduct = productInput()
        except exc.IntegrityError:
            db.session.rollback()
            return jsonify('Something went wrong. Data NOT Posted.')
    return jsonify('Data Posted.')
  

# READ / GET ALL PRODUCTS IN THE DATABASE
@product_views.route('/products/all', methods=["GET"])
def get_productAll():
    pAll = productAll()
    return jsonify(pAll)


# READ / GET 1 PRODUCT IN THE DATABASE BY ID
@product_views.route('/products/<id>', methods=["GET"])
def productOne(id):
    one_product = productSingle(id)
    return jsonify(one_product)


# UPDATE / PUT PRODUCT IN THE DATABASE
@product_views.route('/update/<id>', methods=["PUT"])
def pUpdate(id):
    if request.content_type == 'application/json':
        try:
            updateRecord = productUpdate(id)
        except exc.IntegrityError:
            db.session.rollback()
            return jsonify('Something went wrong. Data NOT Posted.')
    return jsonify('Update Completed.')


# DELETE PRODUCT IN THE DATABASE BY ID
@product_views.route('/delete/<id>', methods=["DELETE"])
def pDelete(id):
    Drecord = productDelete(id)
    return jsonify(Drecord)


# IMAGE
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#ALLOWED_EXTENSIONS = set(['png' , 'jpg' , 'jpeg' , 'gif'])
#def allowed_file(filename):
    #return '.' in filename and filename.rsplit('.' , 1)[1].lower() in ALLOWED_EXTENSIONS


#@product_views.route('/upload', methods=["POST"])
#def upload_image():
    #if 'file' not in request.files:
        #flash ('No File Path')
        #return redirect(request.url)
    #file = request.files['file']
    #if file.filename == '':
        #flash('No image selected for upload')
        #return redirect(request.url)
    #if file and allowed_file(file.filename):
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        ##print('upload_image filename: '+ filename)
        #flash('Image Uploaded Successfully')
        #return render_template('index.html', filename=filename)
    #else:
        #flash('Allowed Images are png, jpg, jpeg, gif')
        #return redirect(request.url)

                              

