from multipledispatch import dispatch
#from backend import Model

class Controller(object):
    def __init__(self, _model, _view):
        self.model = _model
        self.view = _view
    
    def draw_inventory(self): #check this one
        products = self.model.product_get()
        self.view.draw_inventory()
        
    def show_product(self, _product_id): #check this one
        item = self.model.get_item(_product_id)
        self.view.draw_inventory()
        
    def product_get(self, product_id=None):
        return self.model.product_get(product_id)

    def get_products(self):
        return self.model.get_products()
    
    def get_product_keys(self):
        return self.model.get_product_keys()

    def get_unlisted_products(self, store_id):
        return self.model.get_unlisted_products(store_id)
        
    def get_store(self, store_id):
        store = self.model.get_store(store_id)
        return store
    
    def get_stores(self):
        return self.model.get_stores()
    
    def get_quantities(self):
        return self.model.get_quantities()
    
    def get_quantity(self, product_id = None, store_id = None):
        return self.model.get_quantity(product_id, store_id)

    def get_store_quantities(self, _store_id):
        return self.model.get_store_quantities(_store_id)
    
    def get_product_quantities(self, _store_id):
        return self.model.get_product_quantities(_store_id)
    
    #add
    #do not need this function as frontend will not be aware of Product class
    #@dispatch(Product)
    #def product_add(self, product=None):
    #    return self.model.product_add(product)
    def product_add(self, product_dict=None):
        return self.model.product_add(product_dict)
    
    def set_product(self, product_id=None, attrs=None):
        return self.model.set_product(product_id,attrs)
    
    def add_quantity(self,product_id=None, store_id=None, quantity=None):
        return self.model.add_quantity(product_id, store_id, quantity)

    def add_product_quantity(self, _product_quantity = None):
        self.model.add_product_quantity(_product_quantity)
        
    def set_quantity(self, product_id = None, store_id = None, quantity = None):
        self.model.set_quantity(product_id, store_id, quantity)
        
    def query_json(self, query=None):
        return self.model.query_json(query)
    
    def delete_product(self, product_id=None):
        return self.model.delete_product(product_id)
    #********
    #Testing below
    #********
    def query_json2(self, query=None):
        return self.model.query_json2(query)
    
    def query_json3(self, query=None):
        return self.model.query_json3(query)