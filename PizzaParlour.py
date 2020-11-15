from flask import Flask
from flask_restful import Api, Resource, reqparse
import json

app = Flask("Assignment 2")
api = Api(app)

#argument parser when user sends information of a pizza
pizza_args = reqparse.RequestParser()
pizza_args.add_argument("pizzaType", type=str)
pizza_args.add_argument("pizzaSize", type=str)
pizza_args.add_argument("pizzaToppings", action='append', type=str)

#global list containing all the orders in this session
orders = []

#reads json files and returns dictionary based on filename
def read_from_json(file_name: str):
    try:
        with open(file_name) as file:
            return json.loads(file.read())
    except FileNotFoundError: 
        print("couldn't read from file")

#class that food items inherit from in order for them to be serializable to json
class JsonEncode:
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__).replace('\\"',"\"")

#class representing a generic food item
class Food(JsonEncode):
    price: float
    def __init__(self, price):
        self.price = price

#class representing a drink item
class Drink(Food, JsonEncode):
    drink_type: str
    def __init__(self, drink_type: str):
        super().__init__(self.calculatePrice(drink_type))
        self.drink_type = drink_type

    def calculatePrice(self, drink_type):
        drink_prices = read_from_json('foodPrice.json')["drink"]
        # each additional topping is 50 cents
        return drink_prices[drink_type]

#class representing a pizzaType object that all pizza's have to determine their properties
class PizzaType(JsonEncode):
    toppings: [str]
    type_name: str
    def __init__(self, pizza_type: str, toppings: [str]):
        self.type_name = pizza_type
        self.toppings = toppings
    
#class representing a pizza item
class Pizza(Food, JsonEncode):
    toppings: [str]
    pizza_type: PizzaType
    def __init__(self, pizza_type: PizzaType, size: str, toppings: []):
        if toppings is None :
            toppings = []
        super().__init__(self.calculatePrice(pizza_type, size, toppings))
        self.toppings = toppings
        self.pizza_type = pizza_type

    def calculatePrice(self, pizza_type: PizzaType, size: str, toppings: []):
        pizza_prices = read_from_json('foodPrice.json')["pizza"]
        # each additional topping is 50 cents
        return pizza_prices["size"][size] + pizza_prices["type"][pizza_type.type_name] + len(toppings) * 0.5

# class representing an order that contains food items and the total price 
class Order(JsonEncode):
    items: [Food]
    order_num: int
    price: float
    def __init__(self):
        self.price = 0
        self.items = []
        self.order_num = len(orders)

    #add food to order and update price
    def addFood(self, item: Food):
        self.items.append(item)
        self.updatePrice()
    
    def updatePrice(self):
        total = 0
        for item in self.items:
            total += item.price
            print(item.price)
        self.price = total

#Using the factory design pattern, created factory class to help generate our objects 
class Factory:
    @staticmethod
    def create_Drink(drink_type: str):
        return Drink(drink_type)
    
    @staticmethod
    def create_PizzaType(pizza_type, toppings: [str]):
        return PizzaType(pizza_type, toppings)

    @staticmethod        
    def create_Pizza(pizza_type, size, toppings):
        return Pizza(pizza_type, size, toppings)

    @staticmethod
    def create_Order():
        return Order()

#Utility class that constructs our orders based on user input and database data
class JsonUtility:

    # creates a new order and adds to global order list
    @staticmethod
    def add_to_orders(order_dict):
        new_order = Factory.create_Order()
        new_order.addFood(JsonUtility.add_to_orders_helper(order_dict))
        orders.append(new_order)
        return new_order


    #adds items to a new order
    @staticmethod
    def add_to_orders_helper(order_dict: dict):
        pizza_types = read_from_json('pizzaType.json') 
        print(order_dict['pizzaToppings'])
        pizza_type_obj = Factory.create_PizzaType(order_dict['pizzaType'], pizza_types[order_dict['pizzaType']])
        pizza_obj = Factory.create_Pizza(pizza_type_obj, order_dict['pizzaSize'], order_dict['pizzaToppings'])
        return pizza_obj

#api resource object that handles requests to submit an order
class OrderRequest(Resource):
    def post(self):
        #below returns a json string representing an order
        args = pizza_args.parse_args()
        ju = JsonUtility()
        order = ju.add_to_orders(args)
        return order.toJson()
        
api.add_resource(OrderRequest, "/pizza")

if __name__ == "__main__":
    app.run(debug=True) #get rid of debug=True when submitting final version

# run http://127.0.0.1:5000/pizza in web browserd
