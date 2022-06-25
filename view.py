from app import *
import requests
from flask import jsonify

class View():
    def __init__(self):      
        self.controller = None
        
    def set_controller(self, controller=None):
        self.controller = controller
    
    def get_controller(self):
        return self.controller
        
    def dummy(self):
        pass
    
