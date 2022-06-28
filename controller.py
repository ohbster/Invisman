from multipledispatch import dispatch
#from backend import Model

class Controller(object):
    def __init__(self, _model, _view):
        self.model = _model
        self.view = _view
    
    #****************************
    #Common Functions
    #
    #****************************
    def query_json(self, query=None):
        return self.model.query_json(query)
    
    def object_as_dict(self, obj=None):
        return self.model.object_as_dict(obj)
    
    #****************************
    #Product Functions
    #
    #****************************      

    def add_product(self, product_dict=None):
        return self.model.add_product(product_dict)
      
    def get_product(self, product_id=None):
        return self.model.get_product(product_id)

    def get_products(self):
        return self.model.get_products()
    
    def get_product_keys(self):
        return self.model.get_product_keys()

    # def get_unlisted_products(self, store_id):
    #     return self.model.get_unlisted_products(store_id)
    
    def set_product(self, product_id=None, attrs=None):
        return self.model.set_product(product_id,attrs)
    
    def delete_product(self, product_id=None):
        return self.model.delete_product(product_id)
    
    #****************************
    #Store Functions
    #
    #****************************
        
    def get_store(self, store_id):
        store = self.model.get_store(store_id)
        return store
    
    def get_stores(self):
        return self.model.get_stores()
    
    #****************************
    #Quantity Functions
    #
    #****************************
    
    def add_quantity(self,product_id=None, store_id=None, quantity=None):
        return self.model.add_quantity(product_id, store_id, quantity)
    
    def get_quantities(self):
        return self.model.get_quantities()
    
    def get_quantity(self, product_id = None, store_id = None):
        return self.model.get_quantity(product_id, store_id)
        
    def set_quantity(self, product_id = None, store_id = None, quantity = None):
        self.model.set_quantity(product_id, store_id, quantity)
    
    #****************************
    #Relationship Functions
    #
    #****************************
    
    # def get_store_quantities(self, _store_id):
    #     return self.model.get_store_quantities(_store_id)
    #
    # def get_product_quantities(self, _store_id):
    #     return self.model.get_product_quantities(_store_id)
    
    # def add_product_quantity(self, _product_quantity = None):
    #     self.model.add_product_quantity(_product_quantity)
    
    #********
    #Testing below
    #********
    # def query_json2(self, query=None):
    #     return self.model.query_json2(query)
    #
    # def query_json3(self, query=None):
    #     return self.model.query_json3(query)