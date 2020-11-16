import pip._vendor.requests as requests
import json
BASE = "http://127.0.0.1:5000/"


def pizza_input():  
    pizza_types = get_pizza_types()

    print("**IMPORTANT** The types of pizza available include:")
    for types in pizza_types:
        print(types)
    type_pizza = input("Enter the type of pizza you want: ")
    while (type_pizza not in pizza_types):
        for types in pizza_types:
            print(types)
        type_pizza = input("please enter a valid pizza type from above: ")

    size_pizza = input("Enter the size of pizza you want (Valid Options: 's', 'm', 'l'): ")
    while (size_pizza != 's' and size_pizza!='m' and size_pizza != 'l' and size_pizza != '1'):
        size_pizza = input("Enter a valid size (Valid Options: 's', 'm', 'l'): ")
    print("Available toppings include:\n pepperoni \n olives \n tomatoes \n mushrooms\n jalapenos \n chicken \n beef")
    print("please enter the toppings you would like on your pizza. Press enter after each entry. (Type '1' when done): ")
    toppings = []
    topping = input()
    while ( topping != '1'):
        if (topping == 'pepperoni' or topping == 'olives' or topping == 'tomatoes' or topping == 'mushrooms' or topping == 'jalapenos' or topping == 'chicken' or topping == 'beef'):
            toppings.append(topping)
        else:
            print("Invalid topping")
        topping = input()
    pizza = {"pizzaType": type_pizza, "pizzaSize": size_pizza, "pizzaToppings": toppings}
    response = requests.post(BASE + "submit_pizza", pizza)
    print(response.json())
    return pizza

def drink_input():
    drink_types = get_drink_types()
    print("**IMPORTANT** The types of drinks available include:")
    for types in drink_types:
        print(types)
    type_drink = input("Enter the type of drink you want: ")
    while (type_drink not in drink_types):
        for types in drink_types:
            print(types)
        type_drink = input("please enter a valid drink type from above: ")
    drink = {"type": type_drink}
    response = requests.post(BASE + "submit_drink", drink)
    print(response.json())
    return drink

def get_drink_types():
    response = requests.get(BASE + "drink_types")
    return response.json()

def create_order():
    print("Creating a new Order")
    print("What type of item would you like to add to this order?")
    print("Enter 'pizza' to add a Pizza, 'drink' to add a Drink or '1' to cancel this order")
    item_type = input()
    if(item_type != '1'):
        response = requests.put(BASE + "submit_new_order")
        print(response.json())
        while(item_type != '1'):
            if (item_type == 'pizza'):
                pizza_input()
            elif (item_type == 'drink'):
                drink_input()
            else: 
                print("Invalid Item type")
            print("Would you like to enter another item to this order?")
            print("Enter 'pizza' to add another Pizza, 'drink' to add another Drink or '1' to finish this order")
            item_type = input()
        response = requests.get(BASE + "submit_new_order")
        print(response.json())
    else:
        print("order cancelled")

def get_user_input(display_str): # ensures user enters an integer
    cur_input = input(display_str)
    while not cur_input.isdigit():
        cur_input = input("Invalid input "+ display_str)
    return int(cur_input)

def get_orders():
    response = requests.get(BASE + "get_orders")
    return response.json()

def update_order(): # ask the user to re-enter what they want for the same order
    def update_order_helper(order_num):
        orders = (json.loads(get_orders()))["orders_list"] # a list of orders
        update = {"order_to_update": order_num}
        response = requests.post(BASE + "update_order", update)
        print(response.json())

    display_str = "Enter the order number you would like to update: "
    order_num = get_user_input(display_str)
    orders = (json.loads(get_orders()))["orders_list"] # a list of orders
    for order_str in orders:
        order = json.loads(order_str)
        if order["order_num"] == order_num:
            # order is an order dictionary 
            print("What type of item would you like to add to order "+ str(order_num) + "?")
            print("Enter 'pizza' to add a Pizza, 'drink' to add a Drink or '1' to cancel this update")
            item_type = input()
            if(item_type != '1'):
                response = requests.put(BASE + "submit_new_order")
                while(item_type != '1'):
                    if (item_type == 'pizza'):
                        pizza_input()
                    elif (item_type == 'drink'):
                        drink_input()
                    else: 
                        print("Invalid Item type")
                    print("Would you like to enter another item to this order?")
                    print("Enter 'pizza' to add another Pizza, 'drink' to add another Drink or '1' to finish this order")
                    item_type = input()
                print(response.json())
                response = requests.get(BASE + "submit_new_order")
                # remove the new order in orders and replace orders[order_num-1] by the new order
                update_order_helper(order_num)
            else:
                print("update cancelled")
                return 
            return
    print("Your order is not found or you did not modify any order")
    return

def cancel_order():
    display_str = "Enter the order number you would like to cancel: "
    order_num = get_user_input(display_str)
    delete_order = {"order_to_delete": order_num}
    response = requests.post(BASE + "delete_order", delete_order)
    print(response.json())
    return

    
def get_pizza_types():
    response = requests.get(BASE + "pizza_types")
    return response.json()
    
def get_food_prices():
    response = requests.get(BASE + "food_prices")
    return response.json()

def ask_for_menu() -> None: 
    print("Would you like the full menu or search for a specific item? (enter '1' for full menu, '2' for specific item) ")
    user_choice = input()
    while(user_choice != '1' and user_choice != '2'):
        print("Please enter a valid input")
        user_choice = input()
    if user_choice == '1':
        print("Reading the Menu:\n Each pizza size has a base price.\n" +
            "This base price is added to the price for a pizza type to determine the price for the pizza.\n" +
            "Each additional topping adds 50 cents to the price of the pizza.")
        print("Food Prices: ", json.dumps(get_food_prices(), indent=4))
    else:
        print("Do you want the price of a Pizza or a Drink? (enter '1' for pizza, '2' for drink)")
        type_item = input()
        while(type_item != '1' and type_item != '2'):
            print("Please enter either '1' or '2' ")
            type_item = input()
        if (type_item == '1'):
            find_individual_pizza()
        else:
            find_individual_drink()

def find_individual_drink():
    drink_types = get_drink_types()
    print("The types of drinks on are menu include the following:")
    for types in drink_types:
        print(types)
    type_drink = input("Enter the type of drink you want: ")
    while (type_drink not in drink_types):
        type_drink = input("please enter a valid drink type from above: ")
    drink = {"type": type_drink}
    response = requests.post(BASE + "find_drink_price", drink)
    print("The price of this drink is $" + str(response.json()))

def find_individual_pizza():
    pizza_types = get_pizza_types()
    print("The types of pizza available include:")
    for types in pizza_types:
        print(types)
    type_pizza = input("Enter the type of pizza you want to find: ")
    while (type_pizza not in pizza_types):
        type_pizza = input("please enter a valid pizza type from above: ")
    size_pizza = input("Enter the size of pizza you want to find. (Valid Options: 's', 'm', 'l'): ")
    while (size_pizza != 's' and size_pizza!='m' and size_pizza != 'l' and size_pizza != '1'):
        size_pizza = input("Enter a valid size (Valid Options: 's', 'm', 'l'): ")
    print("Available toppings include:\n pepperoni \n olives \n tomatoes \n mushrooms\n jalapenos \n chicken \n beef")
    print("how many additional toppings would you like (enter a number)")
    while (True):
        try :
            toppings = int(input())
            break
        except ValueError:
            print("enter a valid number")
    pizza = {"pizzaType": type_pizza, "pizzaSize": size_pizza, "pizzaToppings": toppings}
    response = requests.post(BASE + "find_pizza_price", pizza)
    print("The price of this pizza is $" + str(response.json()))


def pizza_app() -> None:
    display_str = "\n(Enter the number for each option) 1: menu, 2: order pizza/drink, 3: cancel order, 4: update order 5: ask for pickup/delivery, 6: exit\n"
    u_input = get_user_input(display_str)
    while u_input != 6:
        if u_input == 1:
            ask_for_menu()
        elif u_input == 2:
            create_order()
        elif u_input == 3:
            cancel_order()
        elif u_input == 4:
            update_order()
        else:
            return
        u_input = get_user_input(display_str)



if __name__ == "__main__":
    print('Welcome to the Pizza Order Service')
    pizza_app()
