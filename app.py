from flask import Flask
from flask import url_for
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
def products_get():
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
    return render_template('products_list.html', result=result)

@app.route('/api/product_add', methods=['GET'])
def product():
    fields = inspect(Product).all_orm_descriptors.keys()#get all attributes of Product
    return render_template('product_add.html', fields=fields)

#The Below function can add a product (or any ORM object) to database, and allows for change in schema.
@app.route('/api/product_add', methods=['POST'])
def product_add():
    form_data = request.form
    obj = Product()
    for c in inspect(obj).mapper.column_attrs:
        if c.key != 'id': #ignore id key as this is assigned by database, not form data
            setattr(obj,c.key, form_data[c.key]) #assign the form data to the object's respective attribute
    
    #replace the below code. Should send the object to backend to be added to database. 
    session.add(obj)
    session.commit() #End of function
    
    result = products_get()
    return render_template('products_list.html', result=result)
    