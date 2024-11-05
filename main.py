import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Create an empty DataFrame with specified columns
columns = [
    'Payment_system_provider', 'Payment_number', 'date_time', 'Gross_amount', 'Net_amount',
    'VAT_amount', 'Store_name', 'Status', 'POS', 'Quantity', 'Payment_method',
    'Staff_member', 'Discount', 'Membership_number', 'Payment_Confirmation_Code',
    'Currency', 'Gateway_Fee', 'Card_Type', 'Customer_Segment', 'Card_ID', 'Location',
    'Loyalty_Points', 'Refund_Eligibility'
]

# Function to generate random data for one month for each shop
def generate_data_for_month():
    # Sample data for categorical columns
    payment_providers = ['WorldPay', 'Braintree', 'Shopify']
    store_names = ['Zara', 'Tesco', 'Next', 'Adam Grooming', 'Primark']
    statuses = ['Completed', 'Cancelled']
    pos_options = ['POS1', 'POS2', 'POS3']
    payment_methods = ['Credit Card', 'Debit Card', 'Cash', 'Online']
    staff_members = ['Staff1', 'Staff2', 'Staff3', 'Staff4']
    discounts = [0, 5, 10, 15]  # Discount percentages, but only for members
    currencies = ['GBP']
    card_types = ['Visa', 'MasterCard', 'Amex', 'Discover']
    locations = ['London']

    # Price ranges for each store
    store_price_ranges = {
        'Zara': [89.99, 149.00, 229.00, 119.00, 399.00, 9.99, 45.99, 35.99, 179.00, 69.99, 19.99, 17.99, 22.99, 59.99, 109.00, 79.99],
        'Tesco': [0.49, 1.00, 2.50, 5.00, 10.00, 15.99, 25.00, 19.90, 17.00, 6.99, 0.99, 3.99, 4.99, 8.99, 12.49],
        'Next': [20.00, 25.99, 30.99, 45.99, 55.00, 75.00, 120.00, 150.00, 60.00, 99.99, 15.99, 22.49, 35.00, 42.99, 130.00],
        'Adam Grooming': [35.00, 40.00, 50.00, 60.00, 75.00],
        'Primark': [2.99, 5.99, 9.99, 14.99, 19.99, 25.00, 30.00, 35.00, 3.00, 7.99, 11.49, 16.99, 22.49],
    }

    # Quantity ranges for each store
    store_quantity_ranges = {
        'Zara': (1, 3),         # Customers usually buy 1-3 items at Zara
        'Tesco': (1, 20),       # Customers might buy 1-20 grocery items at Tesco
        'Next': (1, 4),         # Customers usually buy 1-4 items at Next
        'Adam Grooming': (1, 1),# Single service per transaction for grooming
        'Primark': (1, 10),     # Customers might buy 1-10 items at Primark
    }

    # Membership percentage per store
    store_membership_percentages = {
        'Zara': 0.20,           # 20% of customers are members
        'Tesco': 0.10,          # 10% of customers are members
        'Next': 0.30,           # 30% of customers are members
        'Adam Grooming': 0.50,  # 50% of customers are members
        'Primark': 0.15         # 15% of customers are members
    }

    # Stores where VAT is included in the price
    stores_with_vat_included = ['Zara', 'Tesco', 'Next', 'Primark']

    # Dictionary to keep track of card IDs and their usage per store
    store_card_usage = {store: {} for store in store_names}

    # List to hold generated records
    data = []

    # Set the start of the previous month
    today = datetime.now()
    first_day_of_current_month = today.replace(day=1, hour=9, minute=0, second=0, microsecond=0)
    start_date = first_day_of_current_month - timedelta(days=1)
    start_date = start_date.replace(day=1)


    for store_name in store_names:
        # Set initial timestamp for transactions based on store's schedule
        current_time = start_date
        end_time = start_date + timedelta(days=30)

        while current_time < end_time:
            # Ensure the store's transactions occur only within their operational hours
            if store_name == 'Tesco':
                if current_time.hour < 9:
                    current_time = current_time.replace(hour=9, minute=0, second=0)
                elif current_time.hour >= 23:
                    current_time = current_time.replace(hour=9, minute=0, second=0) + timedelta(days=1)
                    continue

                interval_minutes = random.randint(4, 5)
                num_transactions = random.randint(2, 3)

            elif store_name == 'Adam Grooming':
                if current_time.hour < 9:
                    current_time = current_time.replace(hour=9, minute=0, second=0)
                elif current_time.hour >= 20:
                    # Move to the next day at 9 AM if it's past 8 PM
                    current_time = current_time.replace(hour=9, minute=0, second=0) + timedelta(days=1)
                    continue

                interval_minutes = 30
                num_transactions = random.randint(2, 3)

            else:
                if current_time.hour < 9:
                    current_time = current_time.replace(hour=9, minute=0, second=0)
                elif current_time.hour >= 23:
                    current_time = current_time.replace(hour=9, minute=0, second=0) + timedelta(days=1)
                    continue

                # Adjust frequency based on the time of day
                if current_time.hour < 12:
                    interval_minutes = random.randint(15, 30)
                elif 12 <= current_time.hour < 17:
                    interval_minutes = random.randint(10, 15)
                else:
                    interval_minutes = random.randint(5, 10)
                num_transactions = 1

            for _ in range(num_transactions):
                generate_transaction(data, store_name, current_time, payment_providers, store_price_ranges,
                                     store_quantity_ranges, store_membership_percentages, stores_with_vat_included,
                                     store_card_usage, statuses, pos_options, payment_methods, staff_members,
                                     discounts, currencies, card_types, locations)
                current_time += timedelta(minutes=interval_minutes)

    # Create DataFrame from the generated data
    df = pd.DataFrame(data, columns=columns)

    return df

def generate_transaction(data, store_name, current_time, payment_providers, store_price_ranges,
                         store_quantity_ranges, store_membership_percentages, stores_with_vat_included,
                         store_card_usage, statuses, pos_options, payment_methods, staff_members,
                         discounts, currencies, card_types, locations):
    payment_system_provider = random.choice(payment_providers)
    payment_number = f'PMT{random.randint(1000, 9999)}'
    formatted_date_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

    quantity_range = store_quantity_ranges[store_name]
    quantity = random.randint(quantity_range[0], quantity_range[1])

    prices = random.choices(store_price_ranges[store_name], k=quantity)
    gross_amount = round(sum(prices), 2)

    vat_rate = 0.20  # Example VAT rate
    if store_name in stores_with_vat_included:
        net_amount = round(gross_amount / (1 + vat_rate), 2)
        vat_amount = round(gross_amount - net_amount, 2)
    else:
        vat_amount = round(gross_amount * vat_rate, 2)
        net_amount = gross_amount

    status = random.choices(statuses, weights=[95, 5], k=1)[0]
    pos = random.choice(pos_options)
    payment_method = random.choices(payment_methods, weights=[30, 10, 50, 10], k=1)[0]
    staff_member = random.choice(staff_members)

    # Determine if this is a member transaction based on the store's membership percentage
    is_member = random.random() < store_membership_percentages[store_name]
    if is_member:
        customer_segment = 'Member'
        membership_number = f'MEM{random.randint(10000, 99999)}'
        discount = random.choice(discounts)  # Assign a discount only if the customer is a member
    else:
        membership_number = 'MEM00000'
        customer_segment = random.choice(['New Customer', 'Returning Customer'])
        discount = 0  # No discount for non-members

    card_id = None
    if payment_method in ['Credit Card', 'Debit Card']:
        card_id = f'CARD{random.randint(1000, 9999)}'
        if card_id in store_card_usage[store_name]:
            customer_segment = 'Returning Customer'
        else:
            store_card_usage[store_name][card_id] = True
            if not is_member:
                customer_segment = 'New Customer'
    else:
        card_id = 'N/A'

    currency = random.choice(currencies)
    gateway_fee = round(gross_amount * random.uniform(0.01, 0.03), 2)
    card_type = random.choice(card_types)
    location = random.choice(locations)

    # Calculate loyalty points only if the customer is a member
    loyalty_points = int(net_amount / 10) if customer_segment == 'Member' else 0

    # Set refund eligibility only for Zara and Next
    refund_eligibility = 'Eligible' if store_name in ['Zara', 'Next'] else 'Non-Eligible'

    payment_confirmation_code = f'CONF{random.randint(10000, 99999)}'

    data.append([payment_system_provider, payment_number, formatted_date_time, gross_amount, net_amount,
                 vat_amount, store_name, status, pos, quantity, payment_method,
                 staff_member, discount, membership_number, payment_confirmation_code, currency,
                 gateway_fee, card_type, customer_segment, card_id, location, loyalty_points, refund_eligibility])

# Generate the data for one month for each shop
df_monthly_data = generate_data_for_month()

# Display the DataFrame
df_monthly_data.head(), df_monthly_data.shape

df_monthly_data.to_csv('payment_pos.csv')
