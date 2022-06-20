from app import *


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
    result = controller.query_json3(session.query(Store).all())
    if result is not None:
        return result
    else:
        return {'body':[{
            'message': 'No results',
            'response': '200',
            }]}
        
        
        
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