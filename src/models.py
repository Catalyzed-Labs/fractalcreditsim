import datetime
import random

class BalanceSheet:
    def __init__(self, cash=0.0, accounts_receivable=0.0, accounts_payable=0.0, debt=0.0):
        self.cash = cash
        self.accounts_receivable = accounts_receivable
        self.accounts_payable = accounts_payable
        self.debt = debt

    def update_cash(self, amount):
        self.cash += amount

    def update_accounts_receivable(self, amount):
        self.accounts_receivable += amount

    def update_accounts_payable(self, amount):
        self.accounts_payable += amount

    def update_debt(self, amount):
        self.debt += amount

    def __repr__(self):
        return (f"BalanceSheet(cash={self.cash}, accounts_receivable={self.accounts_receivable}, "
                f"accounts_payable={self.accounts_payable}, debt={self.debt})")

class BusinessAttributes:
    def __init__(self, invoices_per_year, customer_averages, on_time_payment_percentage, max_payment_delay):
        """
        Initializes the BusinessAttributes.

        :param invoices_per_year: The average number of invoices the business sends per year.
        :param customer_averages: A dictionary where keys are customer IDs (or references),
                                   and values are the average invoice amounts for those customers.
        :param on_time_payment_percentage: The percentage chance of making a payment on time.
        :param max_payment_delay: The maximum number of days a payment can be delayed.
        """
        self.invoices_per_year = invoices_per_year
        self.customer_averages = customer_averages
        self.on_time_payment_percentage = on_time_payment_percentage
        self.max_payment_delay = max_payment_delay

    def set_customer_average(self, customer, average_amount):
        """
        Sets or updates the average invoice amount for a given customer.

        :param customer: The customer ID (or reference) for which to set the average.
        :param average_amount: The new average invoice amount for the customer.
        """
        self.customer_averages[customer] = average_amount

    def generate_invoice_amount(self, customer):
        """
        Generates a random invoice amount based on the average for the given customer.
        This example assumes a ±20% variation around the average.
        """
        average = self.customer_averages.get(customer, 0)
        if average == 0:
            raise ValueError(f"No average invoice amount defined for customer {customer}")

        variation = 0.2 * average
        return random.normalvariate(average, variation)

    def decides_to_pay_on_time(self):
        """
        Determines if a payment will be made on time based on on_time_payment_percentage.
        """
        return random.random() * 100 <= self.on_time_payment_percentage

    def generate_payment_delay(self):
        """
        Generates a random number of days to delay a payment, up to max_payment_delay.
        """
        return random.randint(1, self.max_payment_delay)

class Business:
    def __init__(self, id, name, attributes: BusinessAttributes):
        self.id = id
        self.name = name
        self.attributes = attributes
        self.balance_sheet = BalanceSheet()
        self.connections = []  # Potential partners or suppliers
        self.customer_list = []  # Stores references to customer Businesses
        self.sent_invoices = []  # Invoices this Business has issued
        self.received_invoices = []  # Invoices this Business has received
        self.payments_made = []  #Payments this business has made

        if not isinstance(attributes, BusinessAttributes):
            raise TypeError("attributes must be an instance of BussinessAttributes")

    def add_customer(self, customer):
        """Add a Business instance to the customer list if not already present."""
        if not isinstance(customer, Business):
            raise TypeError("customer must be an instance of Business")     
        if customer not in self.customer_list:
            self.customer_list.append(customer)

    def issue_invoice(self, recipient, due_date):
        """Generates and sends an invoice to a customer Business."""
        if not isinstance(recipient, Business):
            raise TypeError("recipient must be an instance of Business")
        if due_date < datetime.datetime.now().date():
            raise ValueError("due_date cannot be in the past")
        if recipient not in self.customer_list:
            raise ValueError(f"{recipient.name} is not a customer of {self.name}.")

        amount = self.attributes.generate_invoice_amount(customer=recipient)
        new_invoice = Invoice(issuer=self, recipient=recipient, amount=amount, due_date=due_date)

        # Update balance sheets
        self.balance_sheet.update_accounts_receivable(amount)
        recipient.balance_sheet.update_accounts_payable(amount)

        self.sent_invoices.append(new_invoice)
        recipient.received_invoices.append(new_invoice)
        return new_invoice
        
    def issue_payment(self, invoices, total_amount, payment_date=datetime.datetime.now(), distribution_percentages=None):
        if total_amount <= 0:
            raise ValueError("total_amount must be positive")
        if not invoices:
            raise ValueError("invoices must not be empty")
        
        if distribution_percentages is None:
            # If no distribution is provided, split the payment evenly among invoices
            distribution_percentages = [100 / len(invoices)] * len(invoices)
        
        payment = Payment(self, total_amount, payment_date, invoices, distribution_percentages)
        
        # Update balance sheets
        self.balance_sheet.update_cash(-total_amount)
        self.balance_sheet.update_accounts_payable(-sum(invoice.outstanding_balance for invoice in invoices))
        for invoice in invoices:
            invoice.recipient.balance_sheet.update_cash(invoice.outstanding_balance * (distribution_percentages[invoices.index(invoice)] / 100))
            invoice.recipient.balance_sheet.update_accounts_receivable(-invoice.outstanding_balance * (distribution_percentages[invoices.index(invoice)] / 100))
       
        payment.apply_to_invoices()
        self.payments_made.append(payment)

    def __repr__(self):
        return f"Business(id={self.id}, name='{self.name}', attributes={self.attributes})"

    def get_customer(self, customer_id=None, name=None):
        if customer_id:
            for customer in self.customer_list:
                if customer.id == customer_id:
                    return customer
        elif name:
            for customer in self.customer_list:
                if customer.name == name:
                    return customer
        return random.choice(self.customer_list) if self.customer_list else None

    def get_sent_invoice(self, invoice_id=None, recipient_id=None):
        if invoice_id:
            for invoice in self.sent_invoices:
                if invoice.id == invoice_id:
                    return invoice
        elif recipient_id:
            return [invoice for invoice in self.sent_invoices if invoice.recipient.id == recipient_id]
        return None

    def get_received_invoice(self, invoice_id=None, issuer_id=None):
        if invoice_id:
            for invoice in self.received_invoices:
                if invoice.id == invoice_id:
                    return invoice
        elif issuer_id:
            return [invoice for invoice in self.received_invoices if invoice.issuer.id == issuer_id]
        return None
    
    def get_payment(self, payment_id=None, invoice_id=None):
        if payment_id:
            for payment in self.payments_made:
                if payment.id == payment_id:
                    return payment
        elif invoice_id:
            for payment in self.payments_made:
                if any(invoice.id == invoice_id for invoice in payment.invoices):
                    return payment
        return None

class Invoice:
    _id_counter = 1  # Class variable to auto-increment invoice IDs

    def __init__(self, issuer, recipient, amount, due_date):
        if not isinstance(issuer, Business):
            raise TypeError("issuer must be an instance of Business")
        if not isinstance(recipient, Business):
            raise TypeError("recipient must be an instance of Business")
        if amount <= 0:
            raise ValueError("amount must be positive")

        self.id = Invoice._id_counter
        Invoice._id_counter += 1
        self.issuer = issuer  # Reference to the issuing Business instance
        self.recipient = recipient  # Reference to the receiving Business instance
        self.amount = amount
        self.due_date = due_date
        self.outstanding_balance = amount  # Initially, the outstanding balance is the full invoice amount
        self.paid_date = None
        self.status = 'issued'  # Possible values: 'issued', 'partially_paid', 'paid'
        self.payments = []  # List to track payments made to this invoice

    def make_payment(self, payment_amount, payment_date=None, payment=None):
        """Apply a payment to this invoice, reducing the outstanding balance."""
        self.outstanding_balance -= payment_amount
        if self.outstanding_balance <= 0:
            self.outstanding_balance = 0  # Prevent negative balance
            self.status = 'paid'
            self.paid_date = payment_date or datetime.datetime.now()  # Record when the invoice got fully paid
        else:
            self.status = 'partially_paid'
        if payment:
            self.payments.append(payment)  # Add the payment object to the invoice's list of payments

    def __repr__(self):
        return (f"Invoice(ID: {self.id}, Issuer: {self.issuer.name}, Recipient: {self.recipient.name}, "
                f"Amount: {self.amount}, Outstanding: {self.outstanding_balance}, Due: {self.due_date}, "
                f"Status: {self.status}, Payments: {len(self.payments)})")

class Payment:
    _id_counter = 1

    def __init__(self, payer, amount, payment_date, invoices, distribution_percentages):
        self.id = Payment._id_counter
        Payment._id_counter += 1
        self.payer = payer  # The paying Business instance
        self.amount = amount
        self.payment_date = payment_date
        self.invoices = invoices  # List of Invoice instances the payment will be applied to
        self.distribution_percentages = distribution_percentages  # List of percentages for each invoice
        self.payee_amounts = {}  # Dictionary to track amount paid to each payee

    def apply_to_invoices(self):
        for invoice, percentage in zip(self.invoices, self.distribution_percentages):
            payment_amount = self.amount * (percentage / 100)
            invoice.make_payment(payment_amount, self.payment_date, self) # Pass 'self' as the payment            

    def __repr__(self):
        return (f"Payment(ID: {self.id}, Payer: {self.payer.name}, Amount: {self.amount}, "
                f"Date: {self.payment_date}, Payees: {list(self.payee_amounts.keys())})")
