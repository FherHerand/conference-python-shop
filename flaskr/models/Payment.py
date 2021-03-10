class PaymentInterface:
    
    def pay(self, amount):
        raise Exception("pay(amount) no implementado")

    def name():
        raise Exception("name() no implementado")

class CardPayment(PaymentInterface):
    
    def __init__(self, name, card_number, cvv, expiration_date):
        self._name = name
        self._card_number = card_number
        self._cvv = cvv
        self._expiration_date = expiration_date
        
    def pay(self, amount):
        print('Q{} pagado con Tarjeta'.format(amount))
        return True
    
    def name(self):
        return 'Tarjeta'

class PaypalPayment(PaymentInterface):
    
    def __init__(self, email, password):
        self._email = email
        self._password = password
    
    def pay(self, amount):
        print('Q{} pagado con Paypal'.format(amount))
        return True
    
    def name(self):
        return 'Paypal'
    
    