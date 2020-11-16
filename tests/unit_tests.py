from PizzaParlour import app
import main
import json

# do the following if "pytest --cov-report term --cov=. tests/unit_tests.py" gives error
# sudo apt-get update
# sudo apt-get install python3-pip
# pip3 install pytest-cov  

def test_get_drink_types():
    drink_type_test = {}
    with open('foodPrice.json') as file:
        drink_type_test = json.loads(file.read())
    response = app.test_client().get('/drink_types')

    assert response.status_code == 200
    assert response.data.decode('utf-8').replace('\n', '') == json.dumps(drink_type_test["drink"])

def test_get_food_prices():
    food_price_test = {}
    with open('foodPrice.json') as file:
        food_price_test = json.loads(file.read())
    response = app.test_client().get('/food_prices')

    assert response.status_code == 200
    assert response.data.decode('utf-8').replace('\n', '') == json.dumps(food_price_test)

def test_add_drink():
      drink = {"type": "coke"}
      expected_drink_object = {"price": 1.5, "drink_type": "coke"}
      response = app.test_client().post('/submit_drink', drink)
      assert response.status_code == 200
      assert response.data.decode('utf-8').replace('\n', '') == expected_drink_object

def test_add_pizza():
      pizza ={"pizzaType": 'pepperoni', "pizzaSize": 's', "pizzaToppings": ['mushrooms']}
      expected_pizza_object = {"price": 6.5, "toppings": ["mushrooms"], "pizza_type": {"type_name": "pepperoni", "toppings": ["pepperoni"]}, "size": "s"}
      response = app.test_client().post('/submit_pizza', pizza)
      assert response.status_code == 200
      assert response.data.decode('utf-8').replace('\n', '') == expected_pizza_object
