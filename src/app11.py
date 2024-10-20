from flask_cors import CORS
from datetime import datetime, timedelta
from collections import deque
from utils.create_json import ast_to_dict, dict_to_ast, save_ast_to_json, load_ast_from_json
from utils.collect_operands import collect_operands, collect_operands_for_user_data
from logic.evaluate_condition import evaluate_condition
from logic.add_condition import combine_rules

import os
import requests
from logic.parsing import tokenize, parse_expression
from flask import Flask, jsonify, request, send_from_directory, render_template
app = Flask(__name__, static_folder='../static', template_folder='../templates')
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
rule_number = None
list_of_operand_variables = None
number_of_rules = None
ast_rule_dict = {}

app = Flask(__name__)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/get-rule', methods=['GET'])
def get_rule():
    global number_of_rules
    number_of_rules = request.args.get('number_of_rules')
    
    for i in range (number_of_rules):
        rule = request.args.get('rule')

        path_to_json = f'files/ast_dict_rule_{i+1}.json'
        tokenized_rule = tokenize(rule)
        rule = parse_expression(tokenized_rule)
        ast_dict = ast_to_dict(rule)
        save_ast_to_json(rule,path_to_json)
        ast_rule_dict[f'rule[{i+1}]'] = ast_dict

    return jsonify(ast_rule_dict)


@app.route('/select_rule', methods=['GET'])
def select_rule():
    select_rule_number = request.args.get('rule_number')
    
    global rule_number
    rule_number = select_rule_number

@app.route('/get_operands', methods=['GET'])
def get_operands():
    global rule_number
    global list_of_operand_variables
    rule = load_ast_from_json(r'files/ast_dict_rule_{}.json'.format(rule_number))
    list_of_operand_variables = collect_operands_for_user_data(rule)
    try:
        return jsonify({'list_of_operand_variables': list_of_operand_variables}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/evaluate_user_data', methods=['GET'])
def evaluate_user_data():
    global list_of_operand_variables
    global rule_number
    rule = load_ast_from_json(r'files/ast_dict_rule_{}.json'.format(rule_number))
    user_data_dict = {}
    for i in list_of_operand_variables:
        user_data_dict[i] = request.args.get(i)
    try:
        return jsonify(evaluate_condition(rule, user_data_dict))
    except:
        print(user_data_dict)
        return jsonify(False)

    

@app.route('/add-rule', methods=['GET'])
def add_rule():
    global number_of_rules, ast_rule_dict

    number_of_rules +=1
    number_of_rules_to_combine = request.args.get('number') #maximum 2 only at one time 
    select_operator = request.args.get('operator') #only AND, OR should be selected from the frontend
    list_of_rules_to_combine = []
    for i in range(number_of_rules_to_combine):
        rule_number = request.args.get("rule_number")
        list_of_rules_to_combine.append(rule_number)
    combined_ast = combine_rules(list_of_rules_to_combine, "AND")
    save_ast_to_json(combined_ast,r'files/ast_dict_rule_{}.json'.format(number_of_rules))
    ast_rule_dict[f'rule[{number_of_rules}]'] = combined_ast
    return jsonify(ast_rule_dict[f'rule[{number_of_rules}]'])




    
    



