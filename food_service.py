orderQueue = []

# first operation
def take_order(customer_name, order):
    orderQueue.append((customer_name, order))
    print(f"\n===================================================\n\nQUEUE HAS BEEN UPDATED\nOrder added to queue: {customer_name} - {order}\n")

# second operation
def show_queue():
    if len(orderQueue) == 0:
        print(f"\n===================================================\n(DISPLAY QUEUE)\n\nQueue is currently empty!\n")
        return
    else:
        print("\n===================================================\n(DISPLAY QUEUE)\n\nCurrently preparing:\n")
        for i, (customer_name, order) in enumerate(orderQueue):
            print(f"{i+1}. {customer_name} - {order}")

# third operation
def serve_queue():
    if len(orderQueue) == 0:
        print(f"\n===================================================\n(DISPLAY QUEUE)\n\nQueue is currently empty!\n")
        return
    (customer_name, order) = orderQueue.pop(0)
    print(f"\n===================================================\n(DISPLAY QUEUE)\n\nNow Serving:\n{customer_name} - {order}\n")

# loop
while True:
    print("\n===================================================\n(MENU)\nWhat would you like to do?\n")
    print("1. I'm ready to order!\n2. Is my order ready?\n3. Order up!\n4. Leave")

    user_input = input("\nEnter your destination: ")
    if user_input == "1":
        customer_name = input("\n===================================================\n(ORDER)\nGreat! You are now making an order.\nPlease enter your name: ")
        order = input("\nEnter your order: ")
        take_order(customer_name, order)
    elif user_input == "2":
        show_queue()
    elif user_input == "3":
        serve_queue()
    elif user_input == "4":
        print("\nThank you for using Food Kiosk! Please come again.\n")
        break
    else: 
        print("===================================================\nInvalid Input\nPlease Try Again.\n")