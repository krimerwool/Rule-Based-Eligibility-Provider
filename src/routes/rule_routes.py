from flask import Blueprint, jsonify, request
from utils.create_json import ast_to_dict, save_ast_to_json, load_ast_from_json
from utils.collect_operands import collect_operands_for_user_data
from logic.evaluate_condition import evaluate_condition
from logic.add_condition import combine_rules
from logic.parsing import tokenize, parse_expression

rule_routes = Blueprint('rule_routes', __name__)

rule_number = None
list_of_operand_variables = None
number_of_rules = None
ast_rule_dict = {}


@rule_routes.route('/get-rule', methods=['GET'])
def get_rule():
    global number_of_rules, ast_rule_dict
    number_of_rules = int(request.args.get('number_of_rules'))
    
    for i in range(number_of_rules):
        rule = request.args.get(f'rule_{i+1}')
        path_to_json = f'files/ast_dict_rule_{i+1}.json'
        tokenized_rule = tokenize(rule)
        parsed_rule = parse_expression(tokenized_rule)
        ast_dict = ast_to_dict(parsed_rule)
        save_ast_to_json(parsed_rule, path_to_json)
        ast_rule_dict[f'rule[{i+1}]'] = ast_dict

    return jsonify(ast_rule_dict)


@rule_routes.route('/select_rule', methods=['GET'])
def select_rule():
    global rule_number
    rule_number = request.args.get('rule_number')
    return jsonify({'selected_rule': rule_number}), 200


@rule_routes.route('/get_operands', methods=['GET'])
def get_operands():
    global rule_number, list_of_operand_variables
    rule = load_ast_from_json(f'files/ast_dict_rule_{rule_number}.json')
    list_of_operand_variables = collect_operands_for_user_data(rule)
    
    try:
        return jsonify({'list_of_operand_variables': list_of_operand_variables}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@rule_routes.route('/evaluate_user_data', methods=['GET'])
def evaluate_user_data():
    global list_of_operand_variables, rule_number
    rule = load_ast_from_json(f'files/ast_dict_rule_{rule_number}.json')
    user_data_dict = {operand: request.args.get(operand) for operand in list_of_operand_variables}

    try:
        result = evaluate_condition(rule, user_data_dict)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@rule_routes.route('/add-rule', methods=['GET'])
def add_rule():
    global number_of_rules, ast_rule_dict
    number_of_rules += 1
    number_of_rules_to_combine = int(request.args.get('number'))
    select_operator = request.args.get('operator')

    list_of_rules_to_combine = [request.args.get(f"rule_number_{i+1}") for i in range(number_of_rules_to_combine)]
    
    combined_ast = combine_rules(list_of_rules_to_combine, select_operator)
    save_ast_to_json(combined_ast, f'files/ast_dict_rule_{number_of_rules}.json')
    ast_rule_dict[f'rule[{number_of_rules}]'] = combined_ast
    
    return jsonify(ast_rule_dict[f'rule[{number_of_rules}]']), 200
