# from flask_cors import CORS
# from datetime import datetime, timedelta
# from collections import deque
# from utils.create_json import ast_to_dict, dict_to_ast, save_ast_to_json, load_ast_from_json
# from utils.collect_operands import collect_operands, collect_operands_for_user_data
# from logic.evaluate_condition import evaluate_condition
# from logic.add_condition import combine_rules
# from logic.parsing import tokenize, parse_expression
# from flask import Flask, jsonify, request, send_from_directory, render_template

# app = Flask(__name__, static_folder='../static', template_folder='../templates')
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# rule_number = None
# list_of_operand_variables = None
# number_of_rules = None
# ast_rule_dict = {}


# @app.route('/static/<path:path>')
# def send_static(path):
#     return send_from_directory('static', path)


# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/get-rule', methods=['GET'])
# def get_rule():
#     global number_of_rules
#     number_of_rules = int(request.args.get('number_of_rules'))  # Typecast to int
    
#     for i in range(number_of_rules):
#         rule = request.args.get(f'rule_{i+1}')
#         path_to_json = f'files/ast_dict_rule_{i+1}.json'
#         tokenized_rule = tokenize(rule)
#         parsed_rule = parse_expression(tokenized_rule)
#         ast_dict = ast_to_dict(parsed_rule)
#         save_ast_to_json(parsed_rule, path_to_json)
#         ast_rule_dict[f'rule[{i+1}]'] = ast_dict

#     return jsonify(ast_rule_dict)


# @app.route('/select_rule', methods=['GET'])
# def select_rule():
#     global rule_number
#     rule_number = request.args.get('rule_number')
#     return jsonify({'selected_rule': rule_number}), 200  # Added return


# @app.route('/get_operands', methods=['GET'])
# def get_operands():
#     global rule_number, list_of_operand_variables
#     rule = load_ast_from_json(f'files/ast_dict_rule_{rule_number}.json')
#     list_of_operand_variables = collect_operands_for_user_data(rule)
#     try:
#         return jsonify({'list_of_operand_variables': list_of_operand_variables}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @app.route('/evaluate_user_data', methods=['GET'])
# def evaluate_user_data():
#     global list_of_operand_variables, rule_number
#     rule = load_ast_from_json(f'files/ast_dict_rule_{rule_number}.json')
#     user_data_dict = {}
    
#     for operand in list_of_operand_variables:
#         user_data_dict[operand] = request.args.get(operand)
    
#     try:
#         result = evaluate_condition(rule, user_data_dict)
#         return jsonify(result), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @app.route('/add-rule', methods=['GET'])
# def add_rule():
#     global number_of_rules, ast_rule_dict
#     number_of_rules += 1
#     number_of_rules_to_combine = int(request.args.get('number'))  # Typecast to int
#     select_operator = request.args.get('operator')  # Get operator from frontend

#     list_of_rules_to_combine = []
#     for i in range(number_of_rules_to_combine):
#         rule_number = request.args.get(f"rule_number_{i+1}")
#         list_of_rules_to_combine.append(rule_number)

#     combined_ast = combine_rules(list_of_rules_to_combine, select_operator)  # Use selected operator
#     save_ast_to_json(combined_ast, f'files/ast_dict_rule_{number_of_rules}.json')
#     ast_rule_dict[f'rule[{number_of_rules}]'] = combined_ast
    
#     return jsonify(ast_rule_dict[f'rule[{number_of_rules}]']), 200


# if __name__ == '__main__':
#     app.run(debug=True)



from flask import send_from_directory
from config import create_app
from routes.rule_routes import rule_routes

app = create_app()

# Register blueprint for rule routes
app.register_blueprint(rule_routes)

# Serve static files like JS, CSS, and images if necessary
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Serve the React app if needed (optional, if you want Flask to serve the built React app)
@app.route('/')
def serve_react_app():
    return send_from_directory('../iterative_rule/build', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
