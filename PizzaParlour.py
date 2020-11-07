from flask import Flask
from flask_restful import Api, Resource
import json


app = Flask("Assignment 2")
api = Api(app)

class Food:
    price: float
    def __init__(self, price):
        self.price = price


class Drink(Food):
    pass

class PizzaType:
    preparation_instructions: str
    type_name: str
    def __init__(self):
        self.type_name = 'default'
        self.preparation_instructions = 'default'

class Pizza(Food):
    toppings: [str]
    pizza_type: PizzaType
    def __init__(self, type: PizzaType): #dependency injection use for Object PizzaType
        super().__init__(5.00) #TODO: hardecoded for testing purposes currently, change later
        self.toppings = ['sample toppings']
        self.pizza_type = type
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class Order:
    items: [Food]
    def __init__(self):
        self.items = [Pizza(PizzaType())] #TODO: hardecoded for testing purposes currently, change later
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class Intro(Resource):

    def get(self):
        #below returns a json string representing an order
        order = Order()
        jsonStr = json.dumps(order.toJson())
        print(jsonStr)
        print(json.loads(jsonStr))
        return jsonStr

api.add_resource(Intro, "/pizza")


if __name__ == "__main__":
    app.run(debug=True) #get rid of debug=True when submitting final version

# run http://127.0.0.1:5000/pizza in web browser
