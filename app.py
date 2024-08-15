from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from rules import *
import streamlit as st
import pandas as pd

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

#function to create and use rules
def home():
    st.title("Rule Engine")
    with st.form("my_form"):
        st.write("#### RULE DETAILS")
        new_rule_name=st.text_input("ENTER NAME OF NEW RULE").strip()
        db_rule_names=[rule['Rule Name'].upper() for rule in mongo.db.inventory.find()]
        check=False
        if new_rule_name.upper() in db_rule_names:
            check=True
        rule = st.text_input("ENTER NEW RULE", placeholder ="If multiple rules, enter them seperating by comma").strip()
        st.write("###### OR")
        # rule_name = st.text_input("ENTER RULE NAME", placeholder = "Should be exactly same as it was saved").strip()
        rule_names=[rule['Rule Name'] for rule in mongo.db.inventory.find()]
        rule_name=st.selectbox("Select the rule name to evaluate against", rule_names, index=None, placeholder="Select")

        st.write("#### USER DETAILS")
        age = st.text_input("ENTER AGE", placeholder="Enter an Integer").strip()
        department=st.text_input("ENTER DEPARTMENT").strip()
        salary=st.text_input("ENTER SALARY", placeholder="Enter an Integer").strip()
        experience=st.text_input("ENTER EXPERIENCE", placeholder="Enter an Integer").strip()
        submitted_form = st.form_submit_button("Submit")

    if submitted_form:
        if rule and rule_name:
            return error_rule()
        elif rule and new_rule_name:
            if(check):
                st.error("Rule with this name already exists. Please enter a new name")
                return
            rules=rule.split(',')
            rules=[rule.strip().replace("AND", "and").replace("OR", "or").replace("=", "==")[1:-1] for rule in rules]
            node=combine_rules(rules)
            if(node is None):
                st.error("Invalid rule, please enter a correct rule")
                return
            node_dict = node.to_dict()
            print("Node Dict: ", node_dict)
            mongo.db.inventory.insert_one({'Rule Name':new_rule_name, 'rule':rule, 'AST': node_dict})
            if(age and department and salary and experience):
                context={'age':age, 'department':department, 'salary':salary, 'experience':experience}
                result=evaluate_rule(node, context)
                st.success("Rule added successfully")
                if(result):
                    st.success(result)
                else:
                    st.warning(result)
            else:
                st.error("Provide all the details to evaluate the rule")
                st.success("Rule added successfully")
        elif rule and not new_rule_name:
            st.warning("Please enter the name of the new rule.")
            return
        elif rule_name:
            #search for rule_name in database and get the object
            rule=mongo.db.inventory.find_one({'Rule Name':rule_name})
            if rule:
                if(age and department and salary and experience):
                    context={'age':age, 'department':department, 'salary':salary, 'experience':experience}
                    node=Node.from_dict(rule['AST'])
                    result=evaluate_rule(node, context)
                    if(result):
                        st.success(result)
                    else:
                        st.warning(result)
                else:
                    st.error("Provide all the details to evaluate the rule")
            else:
                st.error("Rule not found")

#function to delete rules
def delete_rules():
    st.title("Delete Rules")
    with st.form("delete_form"):
        # get all rule names from database
        rule_names=[rule['Rule Name'] for rule in mongo.db.inventory.find()]
        # rule_name=st.text_input("Enter the rule name to delete").strip()
        rule_name=st.selectbox("Select the rule name to delete", rule_names, index=None, placeholder="Select")
        submitted_form = st.form_submit_button("Submit")
    if submitted_form:
        if(rule_name):
            rule=mongo.db.inventory.find_one({'Rule Name':rule_name})
            if rule:
                mongo.db.inventory.delete_one({'Rule Name':rule_name})
                st.success("Rule deleted successfully")
            else:
                st.error("Rule not found")
        else:
            st.warning("Please enter the rule name to delete")
    
    st.title("Delete All Rules")
    with st.form("delete_all_rules"):
        st.write("Click the submit button to delete all rules")
        submitted_form = st.form_submit_button("Submit")
        if submitted_form:
            mongo.db.inventory.delete_many({})
            st.success("All rules deleted successfully")


def error_rule():
    st.error("Please enter either new rule or rule name")

#function to display all rules
def display_rules():
    st.title("Display Rules")
    rules = mongo.db.inventory.find()
    d={"Rule Name":[], "Rule":[]}
    for rule in rules:
        d['Rule Name'].append(rule['Rule Name'])
        d['Rule'].append(rule['rule'])
    new = pd.DataFrame.from_dict(d)
    st.table(new)

# function to display AST by rule name
def display_ast():
    st.title("Display AST")
    with st.form("display_ast"):
        # rule_name=st.text_input("Enter the rule name to display AST", placeholder = "Should be exactly same as it was saved").strip()
        rule_names=[rule['Rule Name'] for rule in mongo.db.inventory.find()]    
        rule_name=st.selectbox("Select the rule name to display AST", rule_names, index=None, placeholder="Select")
        submitted_form = st.form_submit_button("Submit")
    if submitted_form:
        if(rule_name):
            rule=mongo.db.inventory.find_one({'Rule Name':rule_name})
            if rule:
                st.write("AST for rule: ", rule_name)
                node=Node.from_dict(rule['AST'])
                st.write(rule['AST'])
            else:
                st.error("Rule not found")
        else:
            st.warning("Please enter the rule name to display AST")

    
with st.sidebar:
    st.write("# Select")

menu = ["Evaluate Rules", "Display Rules and AST", "Delete Rules"]
choice = st.sidebar.selectbox("", menu)

if choice == "Evaluate Rules":
    home()
elif choice == "Display Rules and AST":
    display_rules()
    display_ast()
elif choice=="Delete Rules":
    delete_rules()
