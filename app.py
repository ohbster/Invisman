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

session = Session()
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

@app.route('/products_gridjs')
def list_products():
    return render_template('ajaxgrid.html')

@app.route(PRODUCT_LIST_ROUTE)
def OLD__list_products():
    result = get_products()
    fields = controller.get_product_keys() #get all attributes of Product
    return render_template('list_products.html', result=result, fields=fields)

@app.route('/add_product', methods=['GET'])
def product_new():
    #to return product keys as json.
    fields = controller.get_product_keys()
    return render_template('add_product.html', fields=fields)

#The Below function can add a product_new (or any ORM object) to database, and allows for change in schema.
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
    #get fields for the update form
    fields = controller.get_product_keys() #Possibly rendundant
    product = controller.get_product(product_id=product_id)
    return render_template('view_product.html',fields=fields, product=product)

@app.route('/delete_product/<product_id>')
def delete_product(product_id=None):
    controller.delete_product(product_id)
    return redirect(PRODUCT_LIST_ROUTE)
