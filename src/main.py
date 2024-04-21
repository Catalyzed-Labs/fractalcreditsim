# main.py
from business_attributes import AttributesMenu
from models import Business, BusinessAttributes
from network import create_network_graph, update_network_graph, visualize_network
import random
import datetime
import networkx as nx
import matplotlib.pyplot as plt

def create_businesses():
    while True:
        try:
            num_businesses = int(input("Enter the number of businesses to create: "))
            if num_businesses <= 0:
                raise ValueError("Number of businesses must be a positive integer.")
            break  # Valid input; exit loop
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
    
    businesses = []

    for i in range(num_businesses):
        print("\nSelect attributes for Business #{}:".format(i + 1))
        print("Choose from A1 to F5.")
        while True:
            selected_attr = input("Enter your choice: ").upper()
            if selected_attr in AttributesMenu.presets:
                break  # Valid input; exit loop
            else:
                print("Invalid choice. Please choose from A1 to F5.")
        
        attributes = AttributesMenu.get_attribute(selected_attr)
        businesses.append(Business(id=i, name=f"Business {i + 1}", attributes=attributes))

    return businesses

def adjust_invoice_amount(issuer, recipient):
    # Basic idea: Larger businesses can issue larger invoices, but also consider the recipient's size
    base_amount = random.randint(1_000, 10_000)  # Base range for invoice amounts

    # Adjust based on the issuer's volume: fewer invoices mean potentially larger amounts per invoice
    issuer_adjustment = 365 / issuer.attributes.invoices_per_year

    # Adjust based on the recipient's ability to handle invoices
    recipient_adjustment = recipient.attributes.invoices_per_year / 365

    # Combine adjustments into a final invoice amount, ensuring it's within a reasonable range
    invoice_amount = base_amount * issuer_adjustment * recipient_adjustment
    invoice_amount = max(1_000, min(invoice_amount, 100_000))  # Ensure amount is between 1k and 100k

    return invoice_amount

def setup_network(businesses):
    print("\nSetting up customer relationships...")
    # Example: Asking if user wants to manually define relationships
    while True:
        response = input("Do you want to manually define customer relationships? (yes/no): ").lower()
        if response in ['yes', 'no']:
            break
        else:
            print("Invalid response. Please answer with 'yes' or 'no'.")

    if response == 'yes':
        # Hypothetical user input for defining relationships
        # Implement specific error checking relevant to how you design this interaction
        pass


    potential_customers_pairs = []
    # Step 1: Gather potential customer pairs, avoiding mutual relationships
    for business in businesses:
        other_businesses = [b for b in businesses if b != business]
        for potential_customer in other_businesses:
            if (potential_customer, business) not in potential_customers_pairs:
                potential_customers_pairs.append((business, potential_customer))

    # Randomly shuffle the list to simulate random selection of customer relationships
    random.shuffle(potential_customers_pairs)

    # Step 2: Establish customer relationships from the shuffled list
    for business, customer in potential_customers_pairs:
        if customer not in business.customer_list and len(business.customer_list) < len(businesses) - 1:
            business.add_customer(customer)
            # Calculate a realistic average invoice amount based on both businesses
            average_invoice_amount = adjust_invoice_amount(business, customer)
            business.attributes.set_customer_average(customer, average_invoice_amount)

    # Debugging: Print relationships and average invoice amounts
    for business in businesses:
        print(f"{business.name} has customers: {[customer.name for customer in business.customer_list]}")
        for customer in business.customer_list:
            average = business.attributes.customer_averages.get(customer, 'N/A')
            print(f"    Average invoice for {customer.name}: {average}")

def issue_invoices(businesses, simulation_day):
    for business in businesses:
        # Iterate through each customer of the business
        for customer in business.customer_list:
            # Calculate the probability of issuing an invoice to this customer today
            # This calculation assumes a uniform distribution over the year for simplicity
            total_invoices = business.attributes.invoices_per_year
            customer_invoices = total_invoices / len(business.customer_list)
            daily_invoice_probability = customer_invoices / 365.0
            
            # Decide whether to issue an invoice based on the calculated probability
            if random.random() < daily_invoice_probability:
                # Determine the due date for the invoice
                due_date = simulation_day + datetime.timedelta(days=30)  # Example: 30 days from now
                
                # Issue the invoice
                new_invoice = business.issue_invoice(customer, due_date)
                
                # print(f"Day {simulation_day}: {business.name} issued an invoice to {customer.name}")
                # print(f"Day {simulation_day}: Issued Invoice - ID: {new_invoice.id}, Issuer: {new_invoice.issuer.name}, "
                #       f"Recipient: {new_invoice.recipient.name}, Amount: {new_invoice.amount}, "
                #       f"Due Date: {new_invoice.due_date.strftime('%Y-%m-%d')}, Status: {new_invoice.status}")

def process_payments(businesses, simulation_day):
    for business in businesses:
        # Filter out fully paid invoices before processing
        unpaid_invoices = [invoice for invoice in business.received_invoices if invoice.status != 'paid']

        for invoice in unpaid_invoices:
            # Calculate days overdue, if any
            days_overdue = (simulation_day - invoice.due_date).days if simulation_day > invoice.due_date else 0

            # If the invoice is due today or is overdue
            if simulation_day >= invoice.due_date:
                payment_probability = business.attributes.on_time_payment_percentage
                # Adjust probability for late payments if overdue and not yet at max delay
                if days_overdue > 0 and days_overdue <= business.attributes.max_payment_delay:
                    payment_probability /= 2  # Halve the probability for late payments

                # Decide to pay based on the (adjusted) probability
                if random.randint(1, 100) <= payment_probability:
                    # Determine amount to pay (full amount for new, outstanding balance for partial)
                    amount_to_pay = invoice.outstanding_balance
                    business.issue_payment([invoice], amount_to_pay)
                    payment_status = "on time" if days_overdue == 0 else "late"
                    print(f"Day {simulation_day}: {business.name} paid {payment_status} invoice #{invoice.id}.")

                elif days_overdue > business.attributes.max_payment_delay:
                    # Handle cases where the payment is defaulted
                    print(f"Day {simulation_day}: {business.name} has defaulted on invoice #{invoice.id}.")

def print_business_details(businesses, day):
    print(f"\nEnd of Day {day}: Business Details and Balance Sheets\n" + "-"*60)
    for business in businesses:
        # Print the business object itself, which calls its __repr__ method
        print(business)
        
        # Since BalanceSheet is a separate object within each Business,
        # and assuming you want to print it separately, call its __repr__ too
        print(business.balance_sheet, "\n")

def start_simulation(businesses, num_days):
    simulation_start_date = datetime.datetime.now().date()  # Set the simulation's start date
    print("Simulation starting...")
    
    
    
    for day in range(1, num_days + 1):
        simulation_day = simulation_start_date + datetime.timedelta(days = day)
        print(f"Day {day} of {num_days} ({simulation_day})")
        
        # Daily simulation activities
        issue_invoices(businesses, simulation_day)
        process_payments(businesses, simulation_day)
        
        # Optional: Graph update and visualization
        # network_graph = create_network_graph(businesses)
        # update_network_graph(network_graph, businesses, metric='outstanding_invoices')
        # visualize_network(network_graph, day)
    
 
        print_business_details(businesses, day)
       
    print("Simulation completed.")

# Example integration with visualization and dynamic graph update to be implemented as needed.


def main():
    businesses = create_businesses()
    setup_network(businesses)
    while True:
        try:
            num_days = int(input("Enter the number of days to simulate: "))
            if num_days <= 0:
                raise ValueError("The number of days must be a positive integer.")
            break  # Valid input; exit the loop
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

    start_simulation(businesses, num_days)

if __name__ == "__main__":
    main()


