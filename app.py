from flask import Flask
from flask import url_for, redirect, abort
from flask import render_template, request

from sqlalchemy import text, select, inspect
from controller import Controller
from backend import Model
import json
from math import ceil
 
model = Model()
controller = Controller(_model=model)
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

def get_query_string():
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
    return query_string

def get_page_data():
    direction = request.args.get('direction')
    sort = request.args.get('sort')
    try:
        limit = int(request.args.get('limit'))
        if limit is None:
            limit = 25
    except: #limit is None:
        limit = 25
    try:
        page = int(request.args.get('page'))
        if page is None:
            page = 1
    except: # page is None:
        page = 1
    return {'direction':direction,
            'sort':sort,
            'limit':limit,
            'page':page,
        }

def query_page_data(route=None,add_route=None, properties=None):
    query_string = get_query_string()
    page_data = get_page_data() 
    
    query = controller.query_product(query_string,page_data['sort'],page_data['direction'],paginate=True)
    result = controller.paginate(query['query'],page_data['limit'],page_data['page'])
    total_pages = ceil(query['count'] / page_data['limit'])
    #dictionaries to send to template
    page_data['total_pages']=total_pages
    query_data={'result':result,
                'properties':properties,
                'sub_route':add_route,
                'route':route,
                # 'sort':sort,
                # 'direction':direction,
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
    properties = controller.product_properties()
    page_data = get_page_data()
    query = controller.query_product(get_query_string(),page_data['sort'],page_data['direction'],paginate=True)
    result = controller.paginate(query['query'],page_data['limit'],page_data['page'])
    total_pages = ceil(query['count'] / page_data['limit'])
    page_data['total_pages']=total_pages
    query_data={'result':result,
                'properties':properties,
                'sub_route':'product',
                'route':PRODUCT_LIST_ROUTE,
                'count':query['count']
                }
    
    return render_template('list_entity.html', query_data=query_data, page_data=page_data)
    
@app.route('/add_product', methods=['GET'])
def new_product():
    #to return product keys as json.
    properties = controller.product_properties()
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
    form_data = request.form
    controller.set_product(product_id=product_id,attrs=form_data)
    return redirect(PRODUCT_LIST_ROUTE)
    
@app.route('/view_product/<product_id>')
def view_product(product_id=None):
    product = controller.get_product(product_id=product_id)
    properties = controller.product_properties()
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
    properties = controller.store_properties()
    page_data = get_page_data()
    query = controller.query_store(get_query_string(),page_data['sort'],page_data['direction'],paginate=True)
    result = controller.paginate(query['query'],page_data['limit'],page_data['page'])
    total_pages = ceil(query['count'] / page_data['limit'])
    page_data['total_pages']=total_pages
    query_data={'result':result,
                'properties':properties,
                'sub_route':'store',
                'route':STORE_LIST_ROUTE,
                'count':query['count']
                }
    
    return render_template('list_entity.html', query_data=query_data, page_data=page_data)
 

@app.route('/view_store/<store_id>')
def view_store(store_id=None):
    return redirect(f'/{store_id}/inventory') #clicking on a store immediately lists its inventory

@app.route('/add_store', methods=['GET'])
def new_store():
    properties = controller.store_properties()
    entity_data={
        'properties':properties,
        'cancel_route':STORE_LIST_ROUTE,
        'submit_route':'/add_store',
        }
    return(render_template('add_entity.html', entity_data=entity_data))

@app.route('/add_store', methods=['POST'])
def add_store():
    form_data = request.form
    controller.add_store(form_data)
    return redirect(STORE_LIST_ROUTE)

#****************************
#Inventory Functions
#
#****************************

@app.route('/<store_id>/inventory')
def list_inventory(store_id=None):
    result = controller.get_inventory(store_id)
    keys = controller.get_inventory_keys()
    #This is wasteful, only need product name. Find way to join tables
    #products = controller.get_listed_products()
    return render_template('list_inventory.html', result=result, keys=keys, store_id=store_id, entity='inventory')

@app.route('/<store_id>/add_inventory')
def new_inventory(store_id=None):
    properties = controller.product_properties()
    #catalog = controller.query(Product)
    catalog = controller.get_unlisted_products(store_id)
    return render_template('add_inventory.html',properties=properties,store_id=store_id,catalog=catalog)

@app.route('/<store_id>/add_inventory',methods=['POST'])
def add_inventory(store_id=None):
    json_data = request.get_json()
    controller.multiadd_inventory(store_id,json_data)
    return redirect(f'/{store_id}/inventory')
    