from tkinter import *
import speech_recognition as sr
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

print("\n===================================================\n(MENU)\nWhat would you like to do?\n")
print("1. I'm ready to order!\n2. Is my order ready?\n3. Order up!\n4. Leave")

# loop
while True:

    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        print("\nListening...")
        audio = r.listen(source)
        try:
            print("\nRecognizing...")
            text = r.recognize_google(audio)
            print("\nYou said: " + text)
            if text == "one":
                customer_name = input("\n===================================================\n(ORDER)\nGreat! You are now making an order.\nPlease enter your name: ")
                order = input("\nEnter your order: ")
                take_order(customer_name, order)
            elif text == "two":
                show_queue()
            elif text == "three":
                serve_queue()
            elif text == "four":
                print("\nThank you for using Food Kiosk! Please come again.\n")
                break
        except Exception as e:
            print(e)
            answer = "\nSorry, I did not get that. Come again?"
            print(answer)