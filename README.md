# SETUP Instructions
Install necessary packages by running `pip3 install -r requirements.txt`

Run the main Flask module by running `python3 PizzaParlour.py`

Run unit tests with coverage by running `pytest --cov-report term --cov=. tests/unit_tests.py`

Do the following if "pytest --cov-report term --cov=. tests/unit_tests.py" gives error:

sudo apt-get update

sudo apt-get install python3-pip

pip3 install pytest-cov  

Run the CLI with `python3 main.py`

# Pair Programming Process
For this assignment, we pair programmed the two features: submit a new order and asking for the menu.\
## Pair Programming Submit a new Order ##
This feature was the first feature we attempted for this assignment. Before we started, we wrote \
a rough outline on how our objects were going to be related as well as discussing some of the API calls\
we would need. Once we started, since this was our first time using flask, progress was slow and we had\
to go online for some time to learn the basics.\
Tony was the driver for the first pair programming session where he made a proof of concept API call with\
a hard-coded order as well as creating the basic structure of the objects.\
Alex was the driver for the next session where he created a Factory class to create all of our objects.\
He also added a file to store the prices of our items and implemented a post request to create a hardcoded.\
For the final pair programming session of this feature, Tony was again the driver and finished the submit-order\
feature by constructing an order of any item number from user post requests. Some classes were refactored or
augmented to complete this task.\
## Pair Programming asking for the menu ##
Alex was the driver for the first pair programming session of this feature. During this session, a basic command line\
program was formed so that the users could chose what to do. Fetching the entire menu for the user was also accomplished\
during this session.\
For the second session of this feature, Tony was the driver. Creating an option for the user to search the price of a \
specific item was accomplished during this session\
## Pair Programming Reflection ##

