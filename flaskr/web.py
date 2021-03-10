from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required, login_internal_required
from flaskr.db import get_db
from flaskr.models import *

bp = Blueprint('web', __name__, url_prefix='/web')

@bp.route('/')
@login_internal_required
def index():
    db = get_db()
    customers_count = db.execute('''
        SELECT COUNT(*)
        FROM user
    ''').fetchone()[0] or 0
    products_count = db.execute('''
        SELECT COUNT(*)
        FROM product
    ''').fetchone()[0] or 0
    sales_sum = db.execute('''
        SELECT SUM(l.quantity*l.price_unit)
        FROM sale_order_line l
        JOIN sale_order s ON l.order_id = s.id
        WHERE s.state = 'done'
    ''').fetchone()[0] or 0.00
    sales_count = db.execute('''
        SELECT COUNT(*)
        FROM sale_order
        WHERE state = 'done'
    ''').fetchone()[0] or 0
    payments_sum = db.execute('''
        SELECT SUM(amount)
        FROM payment
    ''').fetchone()[0] or 0.00
    payments_count = db.execute('''
        SELECT COUNT(*)
        FROM payment
    ''').fetchone()[0] or 0
    
    return render_template('web/index.html',
                           customers_count=customers_count,
                           products_count=products_count,
                           sales_sum=sales_sum, sales_count=sales_count,
                           payments_sum=payments_sum, payments_count=payments_count)

@bp.route('/user')
@login_internal_required
def user():
    db = get_db()
    users = db.execute('''
        SELECT *
        FROM user
        WHERE type='internal'
        ORDER BY name
    ''').fetchall()
    return render_template('web/user.html', users=users)

@bp.route('/sale')
@login_internal_required
def sale():
    db = get_db()
    sales = db.execute('''
        SELECT 
            s.*,
            u.name as customer_name,
            (SELECT
                SUM(quantity*price_unit)
                FROM sale_order_line
                WHERE order_id=s.id
            ) as total
        FROM sale_order s
        JOIN user u ON s.customer_id = u.id
        ORDER BY s.date
    ''').fetchall()
    return render_template('web/sale.html', sales=sales)

@bp.route('/payment')
@login_internal_required
def payment():
    db = get_db()
    payments = db.execute('''
        SELECT p.*, s.id as order_name
        FROM payment p
        JOIN sale_order s ON p.order_id = s.id
        ORDER BY p.date
    ''').fetchall()
    return render_template('web/payment.html', payments=payments)

@bp.route('/customer')
@login_internal_required
def customer():
    db = get_db()
    customers = db.execute('''
        SELECT *
        FROM user
        ORDER BY name
    ''').fetchall()
    return render_template('web/customer.html', customers=customers)

@bp.route('/product')
@login_internal_required
def product():
    db = get_db()
    products = db.execute('''
        SELECT p.*, pc.name as category_name
        FROM product p
        JOIN product_category pc ON p.category_id = pc.id
        ORDER BY p.name
    ''').fetchall()
    return render_template('web/product.html', products=products)

@bp.route('/product_category')
@login_internal_required
def product_category():
    db = get_db()
    categories = db.execute('''
        SELECT *
        FROM product_category
        ORDER BY name
    ''').fetchall()
    return render_template('web/product_category.html', categories=categories)