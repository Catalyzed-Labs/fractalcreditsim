# test_models.py
import unittest
import datetime
import logging
from models import Business, BusinessAttributes, Invoice

class TestBusinessModel(unittest.TestCase):
    def setUp(self):
        self.customer_averages = {}  # Initialize an empty dictionary first
        self.attributes = BusinessAttributes(
            invoices_per_year=365,
            customer_averages=self.customer_averages,
            on_time_payment_percentage=80,
            max_payment_delay=30
        )

        # Create Business instances after initializing BusinessAttributes
        self.business_a = Business(id=1, name='Business A', attributes=self.attributes)
        self.business_b = Business(id=2, name='Business B', attributes=self.attributes)

        # Set average invoice amounts for the Business instances
        self.attributes.set_customer_average(self.business_a, 1000)
        self.attributes.set_customer_average(self.business_b, 2000)

    def test_add_customer(self):
        self.business_a.add_customer(self.business_b)
        self.assertIn(self.business_b, self.business_a.customer_list)

    def test_issue_invoice(self):
        self.business_a.add_customer(self.business_b)
        due_date = datetime.datetime.now() + datetime.timedelta(days=30)
        self.business_a.issue_invoice(self.business_b, due_date)
        self.assertEqual(len(self.business_a.sent_invoices), 1)
        self.assertEqual(len(self.business_b.received_invoices), 1)

    def test_set_customer_average(self):
        new_average = 5000
        self.attributes.set_customer_average('customer_3', new_average)
        self.assertEqual(self.attributes.customer_averages['customer_3'], new_average)

    def test_generate_invoice_amount(self):
        customer = self.business_a  # Use the Business instance instead of a string
        average = self.attributes.customer_averages[customer]
        invoice_amount = self.attributes.generate_invoice_amount(customer)
        self.assertGreaterEqual(invoice_amount, average * 0.8)
        self.assertLessEqual(invoice_amount, average * 1.2)

    def test_decides_to_pay_on_time(self):
        on_time_payments = sum(self.attributes.decides_to_pay_on_time() for _ in range(10000))
        expected_on_time_percentage = self.attributes.on_time_payment_percentage / 100
        self.assertAlmostEqual(on_time_payments / 10000, expected_on_time_percentage, delta=0.01)

    def test_generate_payment_delay(self):
        for _ in range(100):
            delay = self.attributes.generate_payment_delay()
            self.assertGreaterEqual(delay, 1)
            self.assertLessEqual(delay, self.attributes.max_payment_delay)

    def test_invoice_and_payment_tracking(self):
        # Simulate issuing an invoice and making a payment
        self.business_a.add_customer(self.business_b)
        due_date = datetime.datetime.now() + datetime.timedelta(days=30)
        invoice = self.business_a.issue_invoice(self.business_b, due_date)
        self.business_b.issue_payment([invoice], invoice.amount)
        
        logging.info(f"Invoices for Business A (sender): {self.business_a.sent_invoices}")
        logging.info(f"Invoices for Business B (receiver): {self.business_b.received_invoices}")
        
        # Verify that the invoice and payment are tracked correctly
        self.assertIn(invoice, self.business_a.sent_invoices, "Invoice should be in the sender's sent invoices list")
        self.assertIn(invoice, self.business_b.received_invoices, "Invoice should be in the receiver's received invoices list")
        self.assertTrue(invoice.status=="paid", "Invoice should be marked as paid")

if __name__ == '__main__':
    unittest.main()