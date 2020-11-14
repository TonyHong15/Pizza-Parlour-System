from flask import Flask
from flask_restful import Api, Resource, reqparse
import json


app = Flask("Assignment 2")
api = Api(app)

pizza_args = reqparse.RequestParser()
pizza_args.add_argument("pizzaType", type=str)
pizza_args.add_argument("pizzaSize", type=str)
pizza_args.add_argument("pizzaToppings", action='append', type=str)

orders = []

foodPrice = {}
with open('foodPrice.json') as f:
    foodPrice = json.loads(f.read())


class Factory:
    def create_Drink():
        return Drink(price, drink_type)

    def create_PizzaType(pizza_type):
        return PizzaType(pizza_type)
        
    def create_Pizza(pizza_type, size, toppings):
        return Pizza(pizza_type, size, toppings)

    def create_Order(order):
        return Order(order)


class JsonEncode:
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__).replace('\\"',"\"")

class Food(JsonEncode):
    price: float
    def __init__(self, price):
        self.price = price

class Drink(Food, JsonEncode):
    drink_type: []
    def __init__(self, price, drink_type):
        super().__init__(price)
        self.drink_type = drink_type

class PizzaType(JsonEncode):
    toppings: [str]
    type_name: str
    def __init__(self, pizza_type):
        self.type_name = pizza_type
        self.preparation_instructions = 'default'
    

class Pizza(Food, JsonEncode):
    toppings: [str]
    pizza_type: PizzaType
    def __init__(self, type: PizzaType, size: str, toppings: []): #dependency injection use for Object PizzaType
        super().__init__(5.00) #TODO: hardcoded for testing purposes currently, change later
        self.toppings = ['sample toppings']
        self.pizza_type = type


class Order(JsonEncode):
    items: [Food]
    order_num: int
    def __init__(self, order: []):
        self.items = order
        # self.items = [Pizza(PizzaType())] #TODO: hardcoded for testing purposes currently, change later
        self.order_num = len(orders)


class JsonUtility():
    
    def add_to_orders(self, order_dict):
        print(order_dict)
        pizza_obj = self.add_to_orders_helper(order_dict)

        new_order = Factory.create_Order([pizza_obj])
        orders.append(new_order)
    
    def add_to_orders_helper(self, order_dict):
        # f = Factory()
        if (True):
            pizza_type_obj = Factory.create_PizzaType(order_dict['pizzaType'])
            pizza_obj = Factory.create_Pizza(pizza_type_obj, order_dict['pizzaSize'], order_dict['pizzaToppings'])
            return pizza_obj


class OrderRequest(Resource):
    def __init__(self):
        pass
        # print(type(self.foodPrice))
        # print(self.foodPrice["Pizza"]["Size"]["M"])

    def post(self):
        #below returns a json string representing an order
        args = pizza_args.parse_args()
        ju = JsonUtility()
        ju.add_to_orders(args)
        return 200
        

api.add_resource(OrderRequest, "/pizza")

if __name__ == "__main__":
    app.run(debug=True) #get rid of debug=True when submitting final version

# run http://127.0.0.1:5000/pizza in web browserd
