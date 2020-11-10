from flask import Flask
from flask_restful import Api, Resource, reqparse
import json


app = Flask("Assignment 2")
api = Api(app)

pizza_args = reqparse.RequestParser()
pizza_args.add_argument("pizzaType", type=str)
pizza_args.add_argument("pizzaSize", type=str)
pizza_args.add_argument("pizzaToppings", action='append', type=str)

class JsonEncode:
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__).replace('\\"',"\"")

class Food(JsonEncode):
    price: float
    def __init__(self, price):
        self.price = price

class Drink(Food, JsonEncode):
    pass

class PizzaType(JsonEncode):
    toppings: [str]
    type_name: str
    def __init__(self):
        self.type_name = 'default'
        self.preparation_instructions = 'default'
    

class Pizza(Food, JsonEncode):
    toppings: [str]
    pizza_type: PizzaType
    def __init__(self, type: PizzaType): #dependency injection use for Object PizzaType
        super().__init__(5.00) #TODO: hardecoded for testing purposes currently, change later
        self.toppings = ['sample toppings']
        self.pizza_type = type


class Order(JsonEncode):
    items: [Food]
    def __init__(self):
        self.items = [Pizza(PizzaType())] #TODO: hardecoded for testing purposes currently, change later


class OrderRequest(Resource):
    foodPrice = {}
    def __init__(self):
        with open('foodPrice.json') as f:
            self.foodPrice = json.loads(f.read())
        # print(type(self.foodPrice))
        # print(self.foodPrice["Pizza"]["Size"]["M"])

    def post(self):
        #below returns a json string representing an order
        args = pizza_args.parse_args()
        print(args)
        return 200
        

api.add_resource(OrderRequest, "/pizza")

if __name__ == "__main__":
    app.run(debug=True) #get rid of debug=True when submitting final version

# run http://127.0.0.1:5000/pizza in web browser
