import pip._vendor.requests as requests
import json
BASE = "http://127.0.0.1:5000/"


# def topping_entries(topping: str):

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
    return pizza

def get_pizza_types():
    response = requests.get(BASE + "pizza_types")
    return response.json()
    
def get_food_prices():
    response = requests.get(BASE + "food_prices")
    return response.json()

def ask_for_menu() -> None: 
    print("Pizza Types: ", json.dumps(get_pizza_types(), indent=4, sort_keys=True))
    print("")
    print("Food Prices: ", json.dumps(get_food_prices(), indent=4))


if __name__ == "__main__":
    print('Welcome to the Pizza Order Service')
    ask_for_menu()
    pizza = pizza_input()
    #response = requests.get(BASE + "pizza_types")
    response = requests.post(BASE + "pizza", pizza)
    print(response.json())