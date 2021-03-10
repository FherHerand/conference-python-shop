from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.models import Sale, Payment, Product

bp = Blueprint('shop', __name__, url_prefix='/shop')

@bp.route('/')
def index():
    db = get_db()
    category_id = request.args.get('category', None, type=str)
    
    if category_id and category_id.isdigit():
        products = db.execute('''
            SELECT p.*, pc.name as category_name
            FROM product p
            JOIN product_category pc ON p.category_id = pc.id
            WHERE p.category_id = ?
            ORDER BY p.name
        ''', (int(category_id),)).fetchall()
    else:
        products = db.execute('''
            SELECT p.*, pc.name as category_name
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
                id = g.cart_order.get_line_id_by_product_id(product.get_id())
                line = Sale.SaleOrderLineModel(product.get_id(), quantity, product.get_price_unit(), g.cart_order.get_id(), id)
                g.cart_order.add_line(line)
            else: 
                order = Sale.SaleOrderModel(g.user['id'], 'draft')
                order.save()
                line = Sale.SaleOrderLineModel(product.get_id(), quantity, product.get_price_unit(), order.get_id(), None)
                order.add_line(line)
                
            return redirect(url_for('shop.cart'))

    return render_template('shop/product.html', product=product)

def get_product(id):
    p = get_db().execute('''
        SELECT *
        FROM product
        WHERE id = ?
    ''', (id,)).fetchone()
    
    if p is None:
        abort(404, "Producto con ID {0} no existe.".format(id))
        
    product = Product.ProductModel(p['code'], p['name'], p['price_unit'], p['image_base64'], p['category_id'], p['id'])

    return product

@bp.route('/cart', methods=('GET', 'POST'))
@login_required
def cart():
    if request.method == 'GET':
        if g.cart_order:
            line_id = request.args.get('id', None)
            if line_id:
                delete = request.args.get('delete', False)
                if delete:
                    g.cart_order.remove_line(line_id)
                else:
                    add = request.args.get('add', 0)
                    g.cart_order.update_qty_line(add, line_id)
                
        lines = []
        total = 0.00
        if g.cart_order:
            lines = g.cart_order.get_lines()
            total = g.cart_order.get_total()
            
        return render_template('shop/cart.html', lines=lines, total=total)
    
@bp.route('/payment', methods=('GET', 'POST'))
@login_required
def payment():
    type = request.args.get('type', None, type=str)
    if request.method == 'POST':
        if g.cart_order:
            total = g.cart_order.get_total()
            
            payment_method = None
            if type == 'card':
                name = request.form['name']
                card_number = request.form['card_number']
                cvv = request.form['cvv']
                year = request.form['year']
                month = request.form['month']
                expiration_date = '{0}/{1}'.format(month, year)
                payment_method = Payment.CardPayment(name, card_number, cvv, expiration_date)
            elif type == 'paypal':
                email = request.form['email']
                password = request.form['password']
                payment_method = Payment.PaypalPayment(email, password)
            
            if payment_method:
                g.cart_order.pay(payment_method)
            
        return redirect(url_for('shop.index'))
    elif request.method == 'GET':
        total = 0.00
        if g.cart_order:
            total = g.cart_order.get_total()
            
        return render_template('shop/payment.html', total=total)