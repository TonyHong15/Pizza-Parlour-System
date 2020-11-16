from flask import Flask
from flask_restful import Api, Resource, reqparse
import json

app = Flask("Assignment 2")
api = Api(app)

#argument parser when user sends information of a pizza
pizza_items_parser = reqparse.RequestParser()
pizza_items_parser.add_argument("pizzaType", type=str)
pizza_items_parser.add_argument("pizzaSize", type=str)
pizza_items_parser.add_argument("pizzaToppings", action='append', type=str)


#argument parser when user sends information of a drink
drink_items_parser = reqparse.RequestParser()       
drink_items_parser.add_argument("type", type=str)

#argument parser when user updates an order
update_items_parser = reqparse.RequestParser()
update_items_parser.add_argument("order_to_update", type=str)

#argument parser when user deletes an order
delete_items_parser = reqparse.RequestParser()
delete_items_parser.add_argument("order_to_delete", type=int)

#file name constants
FOODPRICE_FILE = 'foodPrice.json'
PIZZATYPE_FILE = 'pizzaType.json'

#global list containing all the orders in this session
orders = []
cur_order_num = 0

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
        drink_prices = read_from_json(FOODPRICE_FILE)["drink"]
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
    size: str
    def __init__(self, pizza_type: PizzaType, size: str, toppings: []):
        if toppings is None :
            toppings = []
        super().__init__(self.calculatePrice(pizza_type, size, toppings))
        self.toppings = toppings
        self.pizza_type = pizza_type
        self.size = size

    def calculatePrice(self, pizza_type: PizzaType, size: str, toppings: []):
        pizza_prices = read_from_json(FOODPRICE_FILE)["pizza"]
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
        global cur_order_num
        self.order_num = cur_order_num
        cur_order_num += 1

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

    #creates pizza to add to a new order
    @staticmethod
    def add_pizza_to_orders(order_dict: dict):
        pizza_types = read_from_json(PIZZATYPE_FILE) 
        print(order_dict['pizzaToppings'])
        pizza_type_obj = Factory.create_PizzaType(order_dict['pizzaType'], pizza_types[order_dict['pizzaType']])
        pizza_obj = Factory.create_Pizza(pizza_type_obj, order_dict['pizzaSize'], order_dict['pizzaToppings'])
        return pizza_obj
    #creates drink to add to a new order
    @staticmethod
    def add_drink_to_orders(order_dict: dict):
        drink = Factory.create_Drink(order_dict['type'])
        return drink


class AddPizzaToOrder(Resource):
    def post(self):
        args = pizza_items_parser.parse_args()
        print(args)
        added_pizza = JsonUtility.add_pizza_to_orders(args)
        orders[len(orders) - 1].addFood(added_pizza)
        return added_pizza.toJson()
        
api.add_resource(AddPizzaToOrder, "/submit_pizza")

class AddDrinkToOrder(Resource):
    def post(self):
        args = drink_items_parser.parse_args()
        print(args)
        added_drink = JsonUtility.add_drink_to_orders(args)
        orders[len(orders) - 1].addFood(added_drink)
        return added_drink.toJson()

api.add_resource(AddDrinkToOrder, "/submit_drink")

class CreateNewOrder(Resource):
    def put(self):
        new_order = Factory.create_Order()
        orders.append(new_order)
        return new_order.order_num
    def get(self):
        return orders[len(orders) - 1].toJson()

api.add_resource(CreateNewOrder, "/submit_new_order")

class PizzaTypes(Resource):
    def get(self):
        return read_from_json(PIZZATYPE_FILE)

api.add_resource(PizzaTypes, "/pizza_types")

class FoodPrices(Resource):
    def get(self):
        return read_from_json(FOODPRICE_FILE)

api.add_resource(FoodPrices, "/food_prices")

class DrinkTypes(Resource):
    def get(self):
        foods = read_from_json(FOODPRICE_FILE)
        return foods["drink"]

api.add_resource(DrinkTypes, "/drink_types")

class FindPizzaPrice(Resource):
    def post(self):
     args = pizza_items_parser.parse_args()
     print(args)
     pizza = JsonUtility.add_pizza_to_orders(args)
     return pizza.price

api.add_resource(FindPizzaPrice, "/find_pizza_price")

class FindDrinkPrice(Resource):
    def post(self):
        args = drink_items_parser.parse_args()
        print(args)
        drink = JsonUtility.add_drink_to_orders(args)
        return drink.price

api.add_resource(FindDrinkPrice, "/find_drink_price")

class GetOrders(Resource):
    def get(self):
        tmp_orders = []
        for order in orders:
            print(order.toJson())
            tmp_orders.append(order.toJson())
        tmp_dict = {"orders_list": tmp_orders}
        return json.dumps(tmp_dict)

api.add_resource(GetOrders, "/get_orders")

class UpdateOrder(Resource):
    def post(self):
        args = update_items_parser.parse_args()
        order_to_update = args["order_to_update"]        
        print(order_to_update)
        for i in range(len(orders)):
            if order_to_update["order_num"] == i:
                orders[i] = None
        return args.toJson()

api.add_resource(UpdateOrder, "/update_order")

class DeleteOrder(Resource):
    def post(self):
        args = delete_items_parser.parse_args()
        order_to_delete = args["order_to_delete"]    
        if (order_to_delete >= len(orders) or orders[order_to_delete] == None):
            return "Not a valid order"
        orders[order_to_delete] = None
        return "deleted order "+str(order_to_delete)

api.add_resource(DeleteOrder, "/delete_order")

if __name__ == "__main__":
    app.run(debug=True) #get rid of debug=True when submitting final version

# run http://127.0.0.1:5000/pizza in web browserd
