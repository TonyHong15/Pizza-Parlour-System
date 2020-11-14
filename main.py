import pip._vendor.requests as requests
import json
BASE = "http://127.0.0.1:5000/"


# def topping_entries(topping: str):

def pizza_input():  
    type_pizza = input("Enter the type of pizza you want: ")
    size_pizza = input("Enter the size of pizza you want: ")
    print("please enter the toppings you would like on your pizza. Press enter after each entry. (Type '1' when done): ")
    toppings = []
    topping = input()
    while ( topping != '1'):
        toppings.append(topping)
        topping = input()
    pizza = {"pizzaType": type_pizza, "pizzaSize": size_pizza, "pizzaToppings": toppings}
    return pizza


if __name__ == "__main__":
    print('Welcome to the Pizza Order Service')
    pizza = pizza_input()
    # print(pizza["pizzaToppings"])
    response = requests.post(BASE + "pizza", pizza)
    # print(response.json())