# from datetime import datetime

# date_string = "15-Apr-2023 8:10:35p.m".replace("p.m", "PM")
# date_format = "%d-%b-%Y %I:%M:%S%p"

# # Convert string to datetime object
# date_object = datetime.strptime(date_string, date_format)

# # Convert datetime object back to string
# new_date_string = date_object.strftime(date_format)

# print(new_date_string)

# print("current time: ", datetime.now().strftime(date_format))

# order = "2 x L Pizza (Ground Beef, Jalapenio), 20 x Wings (BBQ Sauce), 2 x Honey Garlic Sauce"

# # Split order into items
# items = order.split(", ")

# formatted_items = []
# for item in items:
#     # Split item into quantity and details
#     quantity, details = item.split(" x ", 1)

#     # Check if item has additional details in parentheses
#     if "(" in details:
#         name, extra_details = details.split(" (", 1)
#         extra_details = extra_details.rstrip(")")
#         formatted_item = f"{quantity} x {name} with {extra_details}"
#     else:
#         formatted_item = f"{quantity} x {details}"

#     formatted_items.append(formatted_item)

# formatted_order = ", ".join(formatted_items)

# print(formatted_order)

string1 = "1 x Extra large pizza"
string2 = "$75.92"
spacing = 30  # Set the spacing between the strings

formatted_string = "{:<{}}{}".format(string1, spacing, string2)
print(formatted_string)


string1 = "1 x Chicken gyro"
string2 = "$75.92"
spacing = 30  # Set the spacing between the strings

formatted_string = "{:<{}}{}".format(string1, spacing, string2)
print(formatted_string)
