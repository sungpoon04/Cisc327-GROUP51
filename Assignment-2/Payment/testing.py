def read_database(file_name):
    data_list = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                line_items = line.strip().split()
                data_list.append(line_items)
    except FileNotFoundError:
        print("The file was not found.")
    
    return data_list

# Mock database to validate the user payment
# It is a 2D list with method, card_number, expiration date, name, country and balance stored in each item
payment_data = read_database("database.txt")

# Function to validate card details
def validate_payment():
    for record in payment_data:
        print(record)
    
validate_payment()