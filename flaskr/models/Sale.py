from flaskr.db import get_db

class SaleOrderModel():
    
    def __init__(self, customer_id, state='draft', id=None):
        self._customer_id = customer_id
        self._state = state#draft,payment,done
        self._id = id
        #self._line_ids = []
        
    def add_line(self, line):
        line.save()
        #self._line_ids.append(line)
    
    def get_lines(self):
        lines = get_db().execute('''
            SELECT l.*, p.name as product_name, p.image_base64 as product_image_base64
            FROM sale_order_line l
            JOIN product p ON l.product_id = p.id
            WHERE order_id=?
        ''', (self._id,))
        return lines
    
    def get_id(self):
        return self._id
    
    def save(self):
        db = get_db()
        cur = db.cursor()
        if self._id:
            cur.execute('''
                UPDATE sale_order SET state=? WHERE id=?
            ''', (self._state, self._id,))
        else:
            cur.execute('''
                INSERT INTO sale_order (customer_id, state) VALUES (?, ?)
            ''', (self._customer_id, self._state,))
            self._id = cur.lastrowid
        db.commit()
        
    def paided(self):
        db = get_db()
        if self._id:
            db.execute('''
                UPDATE sale_order SET state=? WHERE id=?
            ''', ('done', self._id,))
        db.commit()
        
class SaleOrderLineModel():
    
    def __init__(self, product_id, quantity, price_unit, order_id, id=None):
        self._product_id = product_id
        self._quantity = quantity
        self._price_unit = price_unit
        self._order_id = order_id
        self._id = id
    
    def save(self):
        db = get_db()
        cur = db.cursor()
        if self._id:
            cur.execute('''
                UPDATE sale_order_line SET quantity=quantity+? WHERE id=?
            ''', (self._quantity, self._id,))
        else:
            cur.execute('''
                INSERT INTO sale_order_line (product_id, quantity, price_unit, order_id) VALUES (?, ?, ?, ?)
            ''', (self._product_id, self._quantity, self._price_unit, self._order_id,))
            self._id = cur.lastrowid
        db.commit()