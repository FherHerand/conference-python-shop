class PaymentInterface:
    
    def pay(self, amount):
        raise Exception("pay(amount) no implementado")

class CreditCardPayment(PaymentInterface):
    pass
    

class PaypalPayment(PaymentInterface):
    
    def pay(self, amount):
        print('Q{} pagado con Paypal'.format(amount))
        return True