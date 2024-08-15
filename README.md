# Rule Engine with AST

## Steps to use the App
After downloading or cloning the repository navigate to the project folder. After that,
1. Install and create a virtual env using the command `virtualenv flask`
> **_Note_**: Make sure that the python version is greater than 3.10
2. Activate the virtual environment using 
> For mac/linux: `source flask/bin/activate`\
> For windows: `.\flask\Scripts\activate`\
> **_Note_**: To deactivate the environment use the command `deactivate`
3. Install the required packages from the `requirements.txt` file using the command `pip install -r requirements.txt`.
4. `main.py` contains the database information.
> I am using MongoDB database, we can have a look into to the data using MongoDB Compass.
> We can download MongoDB community server from https://www.mongodb.com/try/download/community.
5. Run the app using `streamlit run app.py`

## Details of the App

1. I have utilized streamlit to build the UI.
2. We can access `Evaluate Rules`, `Display Rules and AST`, and `Delete Rules` details using the side panel in the application through navigating.
3. `Evaluate Rules/Create Rules`: This page is used to create a new rule and store it in the database and also to evaluate a rule against some given context.
`Rule Details`: It is necessary to give the rule a name, it will help us in accessing it later on.
> In "Enter name of new rule" enter a name that u wish to give to that particular rule which you are going to add. Eg: `Rule1`

> In the next field, "ENTER NEW RULE, if multiple rules, enter them seperating by comma" enter the rules you wish to enter. If there are multiple rules add them seperating by comma. We would consider to have `and` operation between these rules and generate the AST. \
>Eg: "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)",  "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"

**_Note_** An user need to compulsorily enter above two fields or below field to evaluate the context.

> Select a rule from existing set of rules to use.

`User Details`: asks for context to be evaluated by the selected rule
> `Enter Age`, `Enter Department`, `Enter Salary`, `Enter Experience`. \
> User should enter all of the above. \
> Eg: 20, Sales, 30000, 4

4. `Display Rules and AST`: This page helps in displaying all the saved rules and AST's
> `Display Rules`: Displays all the saved rules. \
> `Display AST`: Displays the AST for selected rule.

5. `Delete Rules`: Used to delete rules from the database
> `Delete Rules`: Select a rule to delete. \
> `Delete All Rules`: Press the submit button to delete all the rules in the database.

## Files description

`node.py`: Contains the definition of the node, base for AST. \
`rules.py`: Contains all the functions to create AST from rules provided by the user.  \
`requirements.txt`: Contains all the libraries required by the app to run, should be installed before running the app. \
`app.py`: Contains functions for adding rules to the database, displaying AST's and rules, evaluating rules, and deleting rules.

## Database Details

`Database and its collections`: MondoDB database
> myDatabase - database name \
> inventory - collection in the database to store the all the rules

