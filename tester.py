from app import *
import requests
from flask import jsonify
from sqlalchemy import inspect

controller = view.get_controller()

@app.route('/api/test_get_store')
def test_get_store(store_id=1):
    return json.loads(controller.get_store(store_id))

@app.route('/api/test_query_json')
def test_query_json():
    return json.loads(controller.query_json())

@app.route('/api/test_query_json2')
def test_query_json2():
        #return json.loads(controller.query_json2(session.query(Store).all()))
    return json.loads(controller.query_json2(session.query(Store).filter_by(id=1)))
    
@app.route('/api/test_query_json3')
def test_query_json3():
    result = controller.query_json(session.query(Store).all())
    if result is not None:
        return json.loads(result)
    else:
        return {'body':[{
            'message': 'No results',
            'response': '200',
            }]}
        
@app.route('/api/get_json')
def get_json():
    response = requests.get('http://127.0.0.1:5000/api/test_query_json3')
    result = json.loads(response.text)
    return result

@app.route('/test/stores')
def stores_get():
    result = controller.query_json(session.query(Store).all())
    if result is not None:
        return json.loads(result)
    else:
        return {'body':[{
            'message': 'No results',
            'response': '200',
            }]}
        
@app.route('/api/test_list_stores',methods = ['POST', 'GET'])
def test_list_stores():
   response = requests.get('http://127.0.0.1:5000/api/test_query_json3')
   result = json.loads(response.text)
   #result = jsonify(response.text)
   return render_template('list_stores.html',result=result)
        
        
@app.route('/api/test_list_products')
def test_list_products():
    response = requests.get('http://127.0.0.1:5000/api/products')
    result = json.loads(response.text)
    return render_template('list_products.html', result=result)

@app.route('/api/test_product_update')
def test_product_update():
    return controller.get_product(3)

@app.route('/api/test_product_get')
def test_product_get():
    return controller.get_product(1)

@app.route('/api/test_delete/<product_id>')
def test_delete_product(product_id=None):
    return delete_product(product_id)

def query_json2(self, query=None):
        #for item in query(Store).all():
        if query is not None:
            data = {'products':[]}
            for row in query:
                data['products'].append(self.object_as_dict(row))
            return json.dumps(data)
        else:
            return None
    
@app.route('/test/gridjs_test1')            
def gridjs_data1():
    result = get_products()
    fields = controller.get_product_keys() #get all attributes of Product
    return render_template('firstgrid.html', result=result, fields=fields)

@app.route('/test/gridjs_ajax')
def gridjs_ajax():
    result = get_products()
    fields = controller.get_product_keys()
    return render_template('ajaxgrid.html')
            
@app.route('/test/keytype')
def test_get_key_type():
    insp = inspect(Product)
    for x in insp.columns:
        print(f"column: {x.key} type: {x.type}")
    return controller.entity_properties(Product)

@app.route('/test/server_gridjs')
def test_server_gridjs():
    result = get_products()
    keys = controller.get_product_keys() #get all attributes of Product
    return render_template('servergridjs.html', result=result, keys=keys, entity='product')
    

#SCRAP AREA
"""
 def query_json3(self, query=None):
        i = 0
        #testing
        query = session.query(Store)
        data = {'data':[{}]}
        #get the string name of the orm model
        #query_desc = query.column_descriptions[0]['name']
        
        #return the type of the orm model
        query_type = query.column_descriptions[0]['type']
        
        if query.count() < 1:
            return None
        else:
            #print the column names of the orm model
            insp = inspect(query_type)
            for x in insp.all_orm_descriptors.keys():
                print(x)
            for row in query:    
                for column in insp.all_orm_descriptors.keys():
                    data['data'][i][column] = getattr(query,column)
                    i = i + 1
                
                #query_name = query.column_descriptions.name
            return json.dumps(data)   
"""

"""
def query_json2(self):
        #testing purposes
        query = session.query(Store).filter_by(id=1).one()
        
        
        i = 0
        table = 'stores'
        data = {'data':[{}]}
        for column in Store.metadata.tables[table].columns.keys():
            data['data'][i][column] = getattr(query,column)
            i = i + 1
        return json.dumps(data)
"""