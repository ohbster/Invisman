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


#dummy view class
 
model = Model()
view = View()
controller = Controller(_model=model, _view=view)
view.set_controller(controller)

session = Session()
Base.metadata.create_all(engine)
connection = engine.connect()


app = Flask(__name__)

@app.route('/api/products', methods=['GET'])
def products_get(): #*************TODO: Handle this in backend and call it from controller
    result = controller.query_json(session.query(Product).all())
    if result is not None:
        return json.loads(result)
    else:
        return {'body':[{
            'message' : 'No results', 
            'response' : '200',
            }]}

@app.route('/api/products_list')
def products_list():
    result = products_get()
    fields = controller.get_product_keys() #get all attributes of Product
    return render_template('products_list.html', result=result, fields=fields)

@app.route('/api/product_add', methods=['GET'])
def product_new():
    #to return product keys as json.
    fields = controller.get_product_keys()
    return render_template('product_add.html', fields=fields)

#The Below function can add a product_new (or any ORM object) to database, and allows for change in schema.
@app.route('/api/product_add', methods=['POST'])
def product_add():
    form_data = request.form
    controller.product_add(form_data)
    return products_list()

@app.route('/api/product_update/<product_id>', methods=['POST'])
def product_update(product_id=None):
    #need to pass id to this function
    form_data = request.form
    controller.set_product(product_id=product_id,attrs=form_data)
    return products_list()
    
@app.route('/api/product_view/<product_id>')
def product_view(product_id=None):
    #get fields for the update form
    fields = controller.get_product_keys() #Possibly rendundant
    product = controller.product_get(product_id=product_id)
    return render_template('product_view.html',fields=fields, product=product)

@app.route('/api/delete_product/<product_id>')
def delete_product(product_id=None):
    controller.delete_product(product_id)
    return redirect('/api/products_list')
