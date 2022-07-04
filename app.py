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
from math import ceil

 
model = Model()
view = View()
controller = Controller(_model=model, _view=view)
view.set_controller(controller)
#session = Session()
Base.metadata.create_all(engine)
connection = engine.connect()

app = Flask(__name__)

#These variables make it easier to redirect
PRODUCT_LIST_ROUTE = '/products'
STORE_LIST_ROUTE = '/stores'

#****************************
#API Routes
#
#****************************

@app.route('/api/products', methods=['GET'])
def get_products(): 
    key_value_pairs = request.args
    direction = request.args.get('direction')
    sort = request.args.get('sort')
    return controller.query_product(key_value_pairs,sort,direction)
    #return controller.get_entities(Product)
        
@app.route('/api/stores')
def get_stores():
    key_value_pairs = request.args
    direction = request.args.get('direction')
    sort = request.args.get('sort')
    return controller.query_product(key_value_pairs,sort,direction)
    #return controller.get_entities(Store)

#****************************
#Front-end Functions
#
#****************************

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/api')
def api():
    return render_template('api.html')

#****************************
#Product Functions
#
#****************************

@app.route('/products_gridjs')
def gridjs_list_products():
    return render_template('ajaxgrid.html')

@app.route(PRODUCT_LIST_ROUTE)
def list_products():
    #this version includes pagination
    key_value_pairs = request.args #TODO!! omit direction, sort, limit, and page
    direction = request.args.get('direction')
    sort = request.args.get('sort')
    try:
        limit = int(request.args.get('limit'))
    except: #limit is None:
        limit = 25
    try:
        page = int(request.args.get('page'))
    except: # page is None:
        page = 1
    keys = controller.get_product_keys() #get all attributes of Product
    query = controller.query_product(key_value_pairs,sort,direction,paginate=True)
    result = controller.paginate(query['query'],limit,page)
    total_pages = ceil(query['count'] / limit)
    #dictionaries to send to template
    page_data={'limit':limit,
               'page':page,
               'count':query['count'],
               'total_pages':total_pages}
    query_data={'result':result,
                'keys':keys,
                'entity':'product',
                'route':PRODUCT_LIST_ROUTE
                }
    #return render_template('list_entity.html', result=result,keys=keys, entity='product', page_data=page_data)
    return render_template('list_entity.html', query_data=query_data, page_data=page_data)
    
    # result = get_products()
    # keys = controller.get_product_keys() #get all attributes of Product
    # return render_template('list_entity.html', result=result, keys=keys, entity='product')
    

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

#****************************
#Store Functions
#
#****************************

@app.route(STORE_LIST_ROUTE)
def list_stores():
    result = get_stores()
    keys = controller.get_store_keys() #get all attributes of Product
    return render_template('list_entity.html', result=result, keys=keys, entity='store') #include an entity type keys to use
    #only one listing page

@app.route('/view_store/<store_id>')
def view_store(store_id=None):
    return redirect(f'/{store_id}/inventory') #clicking on a store immediately lists its inventory

#****************************
#Inventory Functions
#
#****************************

@app.route('/<store_id>/inventory')
def OLD__list_inventory(store_id=None):
    result = controller.get_inventory(store_id)
    #print(f'result = {result}')
    keys = controller.get_inventory_keys()
    return render_template('list_inventory.html', result=result, keys=keys, store_id=store_id, entity='inventory')

@app.route('/<store_id>/add_inventory')
def new_inventory(store_id=None):
    keys = controller.get_inventory_keys()
    return render_template('add_inventory.html',keys=keys,store_id=store_id)

@app.route('/<store_id>/add_inventory',methods=['POST'])
def add_inventory(store_id=None):
    form_data = request.form
    controller.add_inventory(form_data)
    return redirect(f'/{store_id}/inventory')
    