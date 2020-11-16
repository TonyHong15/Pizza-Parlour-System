# SETUP Instructions
### Note that these instructions are for linux based systems and when running on windows, the '3' in pip3 and python3 are to be omitted
Install necessary packages by running `pip3 install -r requirements.txt`

Run the main Flask module by running `python3 PizzaParlour.py`

Run unit tests with coverage by running `pytest --cov-report term --cov=. tests/unit_tests.py`

Do the following if "pytest --cov-report term --cov=. tests/unit_tests.py" gives error:

sudo apt-get update

sudo apt-get install python3-pip

pip3 install pytest-cov  

Run the CLI with `python3 main.py`

# Pair Programming Process
For this assignment, we pair programmed the two features: submit a new order and asking for the menu.
## Pair Programming Submit a new Order ##
This feature was the first feature we attempted for this assignment. Before we started, we wrote 
a rough outline on how our objects were going to be related as well as discussing some of the API calls
we would need. Once we started, since this was our first time using flask, progress was slow and we had
to go online for some time to learn the basics.\
Tony was the driver for the first pair programming session where he made a proof of concept API call with
a hard-coded order as well as creating the basic structure of the objects.\
Alex was the driver for the next session where he created a Factory class to create all of our objects.
He also added a file to store the prices of our items and implemented a post request to create a hardcoded.\
For the final pair programming session of this feature, Tony was again the driver and finished the submit-order
feature by constructing an order of any item number from user post requests. Some classes were refactored or
augmented to complete this task.
## Pair Programming asking for the menu ##
Alex was the driver for the first pair programming session of this feature. During this session, a basic command line
program was formed so that the users could chose what to do. Fetching the entire menu for the user was also accomplished
during this session.\
For the second session of this feature, Tony was the driver. Creating an option for the user to search the price of a 
specific item was accomplished during this session
## Pair Programming Reflection ##
After undergoing this process of pair programming, we both realized how the added perspective allowed us to catch more mistakes.
We believe also though that had we been able to pair program face to face instead of screen sharing, this process would have been more beneficial.\
Some of the challenges we went through include getting on the same page as the other person as sometimes one person's thought process didn't click
immediately for the other. We also had some trouble coming up with a chunk time where we were both available to really get into this process.\
Overall, this exercise showed us that pair programming has its benefits as well as challenges and that this was a beneficial learning experience for our
future in the software engineering industry.

# Program Design #
Prior to starting our code, we designed a basic object relationship that would govern our back-end server. We had both Drinks and pizza inherit from
a more generic food class. Orders will hold food elements and when accessing each one, we will let polymorphism do its work. Finally, we would have
a global variable hold a list of orders during this session which would act as our in memory storage. \
When coding the backend, we kept the single-reponsibility principle in mind and made sure each method wasn't doing too much, dividing into
helper methods when necessary as well as making each class responsible for one thing.\
We also kept the dependency inversion principle in mind and followed it when we implemented our factory design pattern where we created a class whose
sole responsibility was to create objects. 
## Tools Used ##
We both used VS Code as our code editor for this project. This is because it is a very versatile editor that has plugin support for numerous languages.\
For this assignment, we used the python plugin which beyond giving visual cues also acts as a linter. The two linters that we used are sonarlint and pylint.



