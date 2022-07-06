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
controller = Controller(_model=model)
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
        
@app.route('/api/stores')
def get_stores():
    key_value_pairs = request.args
    direction = request.args.get('direction')
    sort = request.args.get('sort')
    return controller.query_product(key_value_pairs,sort,direction)

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

def query_page_data(model=None,route=None,add_route=None):
    key_value_pairs = request.args
    query_string ={}
    for key in key_value_pairs:
        if key == 'limit':
            pass
        elif key == 'sort':
            pass
        elif key == 'page':
            pass
        elif key == 'direction':
            pass
        else:
            query_string[key]=key_value_pairs[key]
            
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
        
    properties = controller.entity_properties(model)
    query = controller.query(model,query_string,sort,direction,paginate=True)
    result = controller.paginate(query['query'],limit,page)
    total_pages = ceil(query['count'] / limit)
    #dictionaries to send to template
    page_data={'limit':limit,
               'page':page,
               'count':query['count'],
               'total_pages':total_pages}
    query_data={'result':result,
                'properties':properties,
                'sub_route':add_route,
                'route':route,
                'sort':sort,
                'direction':direction,
                }
    return {'page_data':page_data,
            'query_data':query_data}
#****************************
#Product Functions
#
#****************************

@app.route('/products_gridjs')
def gridjs_list_products():
    return render_template('ajaxgrid.html')

@app.route(PRODUCT_LIST_ROUTE)
def list_products():
    data = query_page_data(Product,PRODUCT_LIST_ROUTE,'product')
    return render_template('list_entity.html', query_data=data['query_data'], page_data=data['page_data'])
    
#Will need to send info about key types to properly render the rows, and fields for adding and modifying data.
#I.E. A boolean type should display a check mark, and not a text field reading True or False. Numerical fields 
#should only allow numerical input. Longer strings may need require a multiline text area. 
@app.route('/add_product', methods=['GET'])
def new_product():
    #to return product keys as json.
    properties = controller.entity_properties(Product)
    #return render_template('add_product.html', keys=keys)
    entity_data={
        'properties':properties,
        'cancel_route':PRODUCT_LIST_ROUTE,
        'submit_route':'/add_product',
        }
    return(render_template('add_entity.html', entity_data=entity_data))

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
    entity_data={
        'row':product,
        'properties':properties,
        'cancel_route':PRODUCT_LIST_ROUTE,
        'submit_route':'/update_product',
        'delete_route':'/delete_product',
        }
    
    return render_template('view_entity.html', entity_data=entity_data)

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
    data = query_page_data(Store,STORE_LIST_ROUTE,'store')
    return render_template('list_entity.html', query_data=data['query_data'], page_data=data['page_data'])

@app.route('/view_store/<store_id>')
def view_store(store_id=None):
    return redirect(f'/{store_id}/inventory') #clicking on a store immediately lists its inventory

#****************************
#Inventory Functions
#
#****************************

@app.route('/<store_id>/inventory')
def list_inventory(store_id=None):
    result = controller.get_inventory(store_id)
    keys = controller.get_inventory_keys()
    return render_template('list_inventory.html', result=result, keys=keys, store_id=store_id, entity='inventory')

@app.route('/<store_id>/add_inventory')
def new_inventory(store_id=None):
    properties = controller.product_properties()
    catalog = controller.query(Product)
    return render_template('add_inventory.html',properties=properties,store_id=store_id,catalog=catalog)

@app.route('/<store_id>/add_inventory',methods=['POST'])
def add_inventory(store_id=None):
    json_data = request.get_json()
    controller.multiadd_inventory(store_id,json_data)
    return redirect(f'/{store_id}/inventory')
    