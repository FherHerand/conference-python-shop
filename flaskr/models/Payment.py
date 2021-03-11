from flaskr.db import get_db

class PaymentStrategy:
    
    def pay(self, total):
        raise Exception("pay() No implementado")
    
    def name(self):
        raise Exception("name() No implementado")
    
class CardPaymentStrategy(PaymentStrategy):
    
    def __init__(self, name, card_number, cvv, expiration_date):
        self._name = name
        self._card_number = card_number
        self._cvv = cvv
        self._expiration_date = expiration_date
        
    def pay(self, total):
        #verificacion de los datos con tarjeta
        print('Q{0} con tarjeta'.format(total))
        return True
    
    def name(self):
        return 'Tarjeta'
    
class PaypalPaymentStrategy(PaymentStrategy):
    
    def __init__(self, email, password):
        self._email = email
        self._password = password
        
    def pay(self, total):
        #verificacion de los datos con paypal
        print('Q{0} con paypal'.format(total))
        return True
    
    def name(self):
        return 'Paypal'
    
class PaymentModel():
    
    def __init__(self, name, amount, order_id):
        self._name = name
        self._amount = amount
        self._order_id = order_id
        
    def save(self):
        db = get_db()
        db.execute('''
            INSERT INTO payment(name, amount, order_id) VALUES(?, ?, ?)
        ''', (self._name, self._amount, self._order_id,))
        db.commit()