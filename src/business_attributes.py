# business_attributes.py
from models import BusinessAttributes

class AttributesMenu:
    presets = {
        "A1": BusinessAttributes(
            invoices_per_year=91,
            customer_averages={},  # Adjust as needed; possibly a placeholder for now
            on_time_payment_percentage=100,
            max_payment_delay=0
        ),
        "A2": BusinessAttributes(
            invoices_per_year=123,
            customer_averages={},  # Adjust as needed; possibly a placeholder for now
            on_time_payment_percentage=100,
            max_payment_delay=0
        ),
        "A3": BusinessAttributes(
            invoices_per_year=365,
            customer_averages={},  # Adjust as needed; possibly a placeholder for now
            on_time_payment_percentage=100,
            max_payment_delay=0
        ),
        "A4": BusinessAttributes(
            invoices_per_year=730,
            customer_averages={},  # Adjust as needed; possibly a placeholder for now
            on_time_payment_percentage=100,
            max_payment_delay=0
        ),
        "A5": BusinessAttributes(
            invoices_per_year=1095,
            customer_averages={},  # Adjust as needed; possibly a placeholder for now
            on_time_payment_percentage=100,
            max_payment_delay=0
        ),
        "B1": BusinessAttributes(
            invoices_per_year=91,
            customer_averages={},  # Adjust as needed; possibly a placeholder for now
            on_time_payment_percentage=90,
            max_payment_delay=10
        ),
        "B2": BusinessAttributes(
            invoices_per_year=123,
            customer_averages={},  # Adjust as needed; possibly a placeholder for now
            on_time_payment_percentage=90,
            max_payment_delay=10
        ),
        "B3": BusinessAttributes(
            invoices_per_year=365,
            customer_averages={},  # Adjust as needed; possibly a placeholder for now
            on_time_payment_percentage=90,
            max_payment_delay=10
        ),
        "B4": BusinessAttributes(
            invoices_per_year=730,
            customer_averages={},  # Adjust as needed; possibly a placeholder for now
            on_time_payment_percentage=90,
            max_payment_delay=10
        ),
        "B5": BusinessAttributes(
            invoices_per_year=1095,
            customer_averages={},  # Adjust as needed; possibly a placeholder for now
            on_time_payment_percentage=90,
            max_payment_delay=10
        ),
        "C1": BusinessAttributes(
            invoices_per_year=91,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=80,
            max_payment_delay=20
        ),
        "C2": BusinessAttributes(
            invoices_per_year=123,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=80,
            max_payment_delay=20
        ),
        "C3": BusinessAttributes(
            invoices_per_year=365,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=80,
            max_payment_delay=20
        ),
        "C4": BusinessAttributes(
            invoices_per_year=730,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=80,
            max_payment_delay=20
        ),
        "C5": BusinessAttributes(
            invoices_per_year=1095,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=80,
            max_payment_delay=20
        ),
        "D1": BusinessAttributes(
            invoices_per_year=91,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=70,
            max_payment_delay=30
        ),
        "D2": BusinessAttributes(
            invoices_per_year=123,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=70,
            max_payment_delay=30
        ),
        "D3": BusinessAttributes(
            invoices_per_year=365,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=70,
            max_payment_delay=30
        ),
        "D4": BusinessAttributes(
            invoices_per_year=730,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=70,
            max_payment_delay=30
        ),
        "D5": BusinessAttributes(
            invoices_per_year=1095,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=70,
            max_payment_delay=30
        ),
        "E1": BusinessAttributes(
            invoices_per_year=91,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=60,
            max_payment_delay=40
        ),
       "E2": BusinessAttributes(
            invoices_per_year=123,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=60,
            max_payment_delay=40
        ),
        "E3": BusinessAttributes(
            invoices_per_year=365,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=60,
            max_payment_delay=40
        ),
        "E4": BusinessAttributes(
            invoices_per_year=730,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=60,
            max_payment_delay=40
        ),
        "E5": BusinessAttributes(
            invoices_per_year=1095,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=60,
            max_payment_delay=40
        ),
        "F1": BusinessAttributes(
            invoices_per_year=91,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=50,
            max_payment_delay=50
        ),
        "F2": BusinessAttributes(
            invoices_per_year=123,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=50,
            max_payment_delay=50
        ),
        "F3": BusinessAttributes(
            invoices_per_year=365,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=50,
            max_payment_delay=50
        ),
        "F4": BusinessAttributes(
            invoices_per_year=730,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=50,
            max_payment_delay=50
        ),
        "F5": BusinessAttributes(
            invoices_per_year=1095,
            customer_averages={},  # Adjust as needed
            on_time_payment_percentage=50,
            max_payment_delay=50
        )
    }

    @staticmethod
    def get_attribute(preset_name):
        return AttributesMenu.presets.get(preset_name, None)
