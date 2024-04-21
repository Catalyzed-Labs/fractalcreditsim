# network.py
import networkx as nx
import matplotlib.pyplot as plt

def create_network_graph(businesses):
    network_graph = nx.DiGraph()

    # Add nodes (businesses) to the graph
    for business in businesses:
        network_graph.add_node(business, size=business.balance_sheet.cash, name=business.name)

    return network_graph

def update_network_graph(network_graph, businesses, metric='outstanding_invoices'):
    # Update the node sizes based on balance sheet cash or total outstanding balances
    for business in businesses:
        node_size = business.balance_sheet.cash  # or calculate total outstanding balances
        network_graph.nodes[business]['size'] = node_size

    # Update the edges based on the chosen metric
    for business in businesses:
        for customer in business.customer_list:
            edge_weight = calculate_edge_weight(business, customer, metric)
            network_graph.add_edge(business, customer, weight=edge_weight)

def calculate_edge_weight(business, customer, metric):
    if metric == 'outstanding_invoices':
        outstanding_invoices = business.get_sent_invoice(recipient_id=customer.id)
        total_outstanding = sum(invoice.outstanding_balance for invoice in outstanding_invoices)
        return total_outstanding
    elif metric == 'total_payments':
        total_payments = sum(payment.amount for payment in business.payments_made if any(invoice.recipient == customer for invoice in payment.invoices))
        return total_payments
    elif metric == 'average_payments':
        payments_to_customer = [payment for payment in business.payments_made if any(invoice.recipient == customer for invoice in payment.invoices)]
        if payments_to_customer:
            return sum(payment.amount for payment in payments_to_customer) / len(payments_to_customer)
        else:
            return 0
    else:
        raise ValueError(f"Invalid metric: {metric}")

def visualize_network(network_graph, day):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(network_graph)
    nx.draw(network_graph, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=[v['size'] for v in network_graph.nodes.values()])
    plt.title(f"Business Network - Day {day}")
    plt.show()