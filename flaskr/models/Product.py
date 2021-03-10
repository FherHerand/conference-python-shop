from flaskr.db import get_db

class ProductModel():
    
    def __init__(self, code, name, price_unit, image_base64, category_id, id=None):
        self._code = code
        self._name = name
        self._price_unit = price_unit
        self._image_base64 = image_base64
        self._category_id = category_id
        self._id = id

    def get_code(self):
        return self._code
    
    def get_name(self):
        return self._name
    
    def get_price_unit(self):
        return self._price_unit
    
    def get_category_name(self):
        c = get_db().execute('''
            SELECT *
            FROM product_category
            WHERE id = ?
        ''', (self._category_id,)).fetchone()
        return c['name']

    def get_image_base64(self):
        return self._image_base64

    def get_id(self):
        return self._id  
    
class ProductCategoryModel():
    
    def __init__(self, name, id=None):
        self._name = name
        self._id = id