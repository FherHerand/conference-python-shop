#-*- coding: utf-8 -*-
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.models import Sale

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        type = 'portal'
        db = get_db()
        error = None

        if password != confirm_password:
            error = 'No coinciden'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'El usuario {} ya esta registrado.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (name, username, password, type) VALUES (?, ?, ?, ?)',
                (name, username, generate_password_hash(password), type)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Usuario incorrecto'
        elif not check_password_hash(user['password'], password):
            error = 'Credenciales incorrectas'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('shop.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    g.cart_order = None
    if user_id is None:
        g.user = None
        g.cart_quantity = 0
    else:
        db = get_db()
        g.user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        o = db.execute('''
            SELECT * FROM sale_order WHERE state='draft' AND customer_id = ?
        ''', (user_id,)).fetchone()
        if o:
            g.cart_order = Sale.SaleOrderModel(o['customer_id'], o['state'], o['id'])
            g.cart_quantity = int(db.execute('''
                SELECT SUM(quantity) FROM sale_order_line WHERE order_id = ?
            ''', (o['id'],)).fetchone()[0] or 0)
    
    
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('shop.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def login_internal_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        if g.user['type'] == 'portal':
            return redirect(url_for('shop.index'))
        
        return view(**kwargs)

    return wrapped_view