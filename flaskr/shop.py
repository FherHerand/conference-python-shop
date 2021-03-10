from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.models import Sale, Payment

bp = Blueprint('shop', __name__, url_prefix='/shop')

@bp.route('/')
def index():
    db = get_db()
    category_id = request.args.get('category', None, type=str)
    
    if category_id and category_id.isdigit():
        products = db.execute('''
            SELECT p.id, p.name, p.price_unit, pc.name as category_name
            FROM product p
            JOIN product_category pc ON p.category_id = pc.id
            WHERE p.category_id = ?
            ORDER BY p.name
        ''', (int(category_id),)).fetchall()
    else:
        products = db.execute('''
            SELECT p.id, p.name, p.price_unit, pc.name as category_name
            FROM product p
            JOIN product_category pc ON p.category_id = pc.id
            ORDER BY p.name
        ''').fetchall()
        
    categories = db.execute('''
        SELECT *
        FROM product_category
        ORDER BY name
    ''').fetchall()
    return render_template('shop/index.html', products=products, categories=categories)

@bp.route('/product/<int:id>', methods=('GET', 'POST'))
@login_required
def product(id):
    product = get_product(id)
    if request.method == 'POST':
        quantity = request.form.get('quantity', 1, int)
        error = None

        if not quantity:
            error = 'Cantidad requerida'

        if error is not None:
            flash(error)
        else:
            if g.cart_order:
                db = get_db()
                l = db.execute('''
                    SELECT id FROM sale_order_line WHERE product_id=? AND order_id=?
                ''', (product['id'], g.cart_order.get_id(),)).fetchone()
                if l is not None:
                    id = l[0]
                else:
                    id = None
                line = Sale.SaleOrderLineModel(product['id'], quantity, product['price_unit'], g.cart_order.get_id(), id)
                g.cart_order.add_line(line)
            else: 
                order = Sale.SaleOrderModel(g.user['id'], 'draft')
                order.save()
                line = Sale.SaleOrderLineModel(product['id'], quantity, product['price_unit'], order.get_id(), None)
                order.add_line(line)
                
            return redirect(url_for('shop.cart'))

    return render_template('shop/product.html', product=product)

def get_product(id):
    product = get_db().execute('''
        SELECT p.id, p.name, p.price_unit, pc.name as category_name
        FROM product p
        JOIN product_category pc ON p.category_id = pc.id
        WHERE p.id = ?
    ''', (id,)).fetchone()

    if product is None:
        abort(404, "Producto ID {0} no existe.".format(id))

    return product

@bp.route('/cart', methods=('GET', 'POST'))
@login_required
def cart():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
            error = 'El usuario {} ya esta registrado.'.format(username)

        if error is None:
            db.commit()
            return redirect(url_for('shop.payment'))

        flash(error)
    elif request.method == 'GET':
        db = get_db()
        
        line_id = request.args.get('id', None)
        if line_id:
            delete = request.args.get('delete', False)
            if delete:
                db.execute('''
                    DELETE FROM sale_order_line
                    WHERE id = ?
                ''', (line_id,))
                db.commit()
            else:
                add = request.args.get('add', 0)
                db.execute('''
                    UPDATE sale_order_line
                    SET quantity = CASE 
                        WHEN quantity+? > 0 THEN quantity+?
                        ELSE quantity
                    END
                    WHERE id = ?
                ''', (add, add, line_id,))
                db.commit()
                
        lines = []
        total = 0.00
        if g.cart_order:
            lines = g.cart_order.get_lines()
            total = db.execute('''
                SELECT SUM(quantity*price_unit) FROM sale_order_line WHERE order_id = ?
            ''', (g.cart_order.get_id(),)).fetchone()[0] or 0.00
            
        return render_template('shop/cart.html', lines=lines, total=total)
    
@bp.route('/payment', methods=('GET', 'POST'))
@login_required
def payment():
    type = request.args.get('type', None, type=str)
    if request.method == 'POST':
        total = get_db().execute('''
            SELECT SUM(quantity*price_unit) FROM sale_order_line WHERE order_id = ?
        ''', (g.cart_order.get_id(),)).fetchone()[0] or 0.00
        
        if type == 'card':
            method = Payment.CreditCardPayment()
            success_payment = method.pay(total)
        elif type == 'paypal':
            method = Payment.PaypalPayment()
            success_payment = method.pay(total)
        else:
            success_payment = False
        
        if success_payment:
            #pay = new PaymentModel(total)
            g.cart_order.paided()
            
        
        return redirect(url_for('shop.index'))
    elif request.method == 'GET':
        db = get_db()
        total = 0.00
        if g.cart_order:
            total = db.execute('''
                SELECT SUM(quantity*price_unit) FROM sale_order_line WHERE order_id = ?
            ''', (g.cart_order.get_id(),)).fetchone()[0] or 0.00
            
        return render_template('shop/payment.html', total=total)