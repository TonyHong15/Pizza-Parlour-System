from PizzaParlour import app

# do the following if "pytest --cov-report term --cov=. tests/unit_tests.py" gives error
# sudo apt-get update
# sudo apt-get install python3-pip
# pip3 install pytest-cov  

def test_pizza():
    response = app.test_client().get('/pizza')

    assert response.status_code == 500
    assert response.data == b'Welcome to Pizza Planet!'
