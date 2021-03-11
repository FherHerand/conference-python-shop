from flaskr.models.Payment import PaymentModel
from flaskr.db import get_db

class SaleOrderModel():
    
    def __init__(self, customer_id, state='draft', id=None):
        self._customer_id = customer_id
        self._state = state#draft,payment,done
        self._id = id
        
    def add_line(self, line):
        line.save()
    
    def remove_line(self, line_id):
        db = get_db()
        db.execute('''
            DELETE FROM sale_order_line
            WHERE id = ?
        ''', (line_id,))
        db.commit()
    
    def get_lines(self):
        lines = get_db().execute('''
            SELECT l.*, p.name as product_name, p.image_base64 as product_image_base64
            FROM sale_order_line l
            JOIN product p ON l.product_id = p.id
            WHERE order_id=?
        ''', (self._id,))
        return lines
    
    def update_qty_line(self, add, line_id):
        db = get_db()
        db.execute('''
            UPDATE sale_order_line
            SET quantity = CASE 
                WHEN quantity+? > 0 THEN quantity+?
                ELSE quantity
            END
            WHERE id = ?
        ''', (add, add, line_id,))
        db.commit()
    
    def get_line_id_by_product_id(self, product_id):
        db = get_db()
        l = db.execute('''
            SELECT id FROM sale_order_line WHERE product_id=? AND order_id=?
        ''', (product_id, self._id,)).fetchone()
        
        id = l[0] if l is not None else None
        return id

    def get_total(self):
        db = get_db()
        total = db.execute('''
            SELECT SUM(quantity*price_unit) FROM sale_order_line WHERE order_id = ?
        ''', (self._id,)).fetchone()[0] or 0.00
        return total
    
    def get_quantity(self):
        db = get_db()
        qty = int(db.execute('''
                SELECT SUM(quantity) FROM sale_order_line WHERE order_id = ?
            ''', (self._id,)).fetchone()[0] or 0)
        return qty
        
    def pay(self, payment_method):
        pass
    
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