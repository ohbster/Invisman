from flask import Flask
from flask import url_for, redirect, abort
from flask import render_template, request
from database import Session, engine
from sqlalchemy import text, select, inspect
from controller import Controller
from models import *
from backend import Model
from view import View
from view import *
import json

 
model = Model()
view = View()
controller = Controller(_model=model, _view=view)
view.set_controller(controller)
#session = Session()
Base.metadata.create_all(engine)
connection = engine.connect()

app = Flask(__name__)

#These variables make it easier to 
PRODUCT_LIST_ROUTE = '/products'
STORE_LIST_ROUTE = '/stores'
#****************************
#Product Routes
#
#****************************

#API calls

@app.route('/api/products', methods=['GET'])
def get_products(): #*************TODO: Handle this in backend and call it from controller
    return controller.get_entities(Product)
    # result = controller.query_json(session.query(Product).all())
    # if result is not None:
    #     return json.loads(result)
    # if result is not None:
    #     return result
    # else:
    #     return {'body':[{
    #         'message' : 'No results', 
    #         'response' : '200',
    #         }]}
        
@app.route('/api/stores')
def get_stores():
    return controller.get_entities(Store)

#Front End
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/products_gridjs')
def list_products():
    return render_template('ajaxgrid.html')

@app.route(STORE_LIST_ROUTE)
def OLD__list_stores():
    result = get_stores()
    keys = controller.get_store_keys() #get all attributes of Product
    return render_template('list_entity.html', result=result, keys=keys, entity='store') #include an entity type keys to use
    #only one listing page

@app.route(PRODUCT_LIST_ROUTE)
def OLD__list_products():
    result = get_products()
    keys = controller.get_product_keys() #get all attributes of Product
    return render_template('list_entity.html', result=result, keys=keys, entity='product')

#Will need to send info about key types to properly render the rows, and fields for adding and modifying data.
#I.E. A boolean type should display a check mark, and not a text field reading True or False. Numerical fields 
#should only allow numerical input. Longer strings may need require a multiline text area. 
@app.route('/add_product', methods=['GET'])
def new_product():
    #to return product keys as json.
    keys = controller.get_product_keys()
    return render_template('add_product.html', keys=keys)

#The Below function can add a new_product (or any ORM object) to database, and allows for change in schema.
@app.route('/add_product', methods=['POST'])
def add_product():
    form_data = request.form
    controller.add_product(form_data)
    return redirect(PRODUCT_LIST_ROUTE)

@app.route('/update_product/<product_id>', methods=['POST'])
def update_product(product_id=None):
    #need to pass id to this function
    form_data = request.form
    controller.set_product(product_id=product_id,attrs=form_data)
    return redirect(PRODUCT_LIST_ROUTE)
    
@app.route('/view_product/<product_id>')
def view_product(product_id=None):
    product = controller.get_product(product_id=product_id)
    properties = controller.entity_properties(Product)
    return render_template('view_product.html', product=product, properties=properties)

@app.route('/delete_product/<product_id>')
def delete_product(product_id=None):
    controller.delete_product(product_id)
    return redirect(PRODUCT_LIST_ROUTE)
