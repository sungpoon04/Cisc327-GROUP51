import unittest
from app import validate_payment, read_database

class TestPaymentValidation(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Load database.txt
        cls.payment_data = read_database('database.txt')

    # Note that the values provided are the interpreted versions of the values retrieved from website
    # For example, name "John Smith" would still be converted into "johnsmith" for comparison
    
    #Tests four 4 valid cards in the database.txt
    def test_debit(self):
        method = "debit"
        card_number = "1111111111111111"
        expiration = "0125"
        cvc = "001"
        name_on_card = "johnsmith"
        country = "CA"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNotNone(balance)
        self.assertGreaterEqual(balance, 1244.13)

    def test_credit(self):
        method = "credit"
        card_number = "2222222222222222"
        expiration = "0226"
        cvc = "002"
        name_on_card = "johnsmith"
        country = "CA"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNotNone(balance)
        self.assertGreaterEqual(balance, 1244.13)
        
    def test_visa(self):
        method = "visa"
        card_number = "3333333333333333"
        expiration = "0327"
        cvc = "003"
        name_on_card = "johnsmith"
        country = "US"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNotNone(balance)
        self.assertGreaterEqual(balance, 1244.13)
        
    def test_master(self):
        method = "master"
        card_number = "4444444444444444"
        expiration = "0428"
        cvc = "004"
        name_on_card = "johnsmith"
        country = "US"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNotNone(balance)
        self.assertGreaterEqual(balance, 1244.13)

    # The card is valid, but it has insufficient fund
    def test_insufficient_fund(self):
        method = "debit"
        card_number = "5555555555555555"
        expiration = "0529"
        cvc = "005"
        name_on_card = "johnsmith"
        country = "CA"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNotNone(balance)
        self.assertLess(balance, 1244.13)

    # Everything is valid, but the method
    def test_incorrect_method(self):
        method = "credit"
        card_number = "1111111111111111"
        expiration = "0125"
        cvc = "001"
        name_on_card = "johnsmith"
        country = "CA"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNone(balance)
        
    # Everything is valid, but the number
    def test_incorrect_number(self):
        method = "debit"
        card_number = "1111111122222222"
        expiration = "0125"
        cvc = "001"
        name_on_card = "johnsmith"
        country = "CA"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNone(balance)
        
    # Everything is valid, but the expiration date
    def test_incorrect_expiration(self):
        method = "debit"
        card_number = "1111111111111111"
        expiration = "1299"
        cvc = "001"
        name_on_card = "johnsmith"
        country = "CA"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNone(balance)
        
    # Everything is valid, but the CVC
    def test_incorrect_cvc(self):
        method = "debit"
        card_number = "1111111111111111"
        expiration = "0125"
        cvc = "999"
        name_on_card = "johnsmith"
        country = "CA"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNone(balance)
        
    # Everything is valid, but the name
    def test_incorrect_name(self):
        method = "debit"
        card_number = "1111111111111111"
        expiration = "0125"
        cvc = "001"
        name_on_card = "smithjohn"
        country = "CA"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNone(balance)
        
    # Everything is valid, but the country
    def test_incorrect_country(self):
        method = "debit"
        card_number = "1111111111111111"
        expiration = "0125"
        cvc = "001"
        name_on_card = "johnsmith"
        country = "US"
        
        balance = validate_payment(method, card_number, expiration, cvc, name_on_card, country)
        self.assertIsNone(balance)


if __name__ == '__main__':
    unittest.main()
