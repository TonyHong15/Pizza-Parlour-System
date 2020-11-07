from flask import Flask # if does not work then run: sudo apt install python3-flask

app = Flask("Assignment 2")

@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'

if __name__ == "__main__":
    app.run()

# run http://127.0.0.1:5000/pizza in web browser
