from app import *

controller = view.get_controller()

@app.route('/api/test_get_store')
def test_get_store(store_id=1):
    return controller.get_store(json.dumps(store_id))
    