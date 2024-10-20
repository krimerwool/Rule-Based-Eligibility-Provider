import re
from utils.create_node import Node
from utils.create_json import ast_to_dict, dict_to_ast

def tokenize(rule_string):
    tokens = re.findall(r'\w+\s*=\s*\'\w+\'|\w+\s*[><=]\s*\d+|\(|\)|AND|OR', rule_string)
    return tokens

def parse_condition(condition):
    condition = condition.strip()
    if '>' in condition:
        attribute, value = condition.split('>')
        return lambda data: data[attribute.strip()] > int(value.strip())
    elif '<' in condition:
        attribute, value = condition.split('<')
        return lambda data: data[attribute.strip()] < int(value.strip())
    elif '=' in condition:
        attribute, value = condition.split('=')
        value = value.strip().strip("'")
        return lambda data: data[attribute.strip()] == value

def parse_expression(tokens):
    """ Parse tokens into an AST recursively. """
    stack = []
    
    def create_node(op_type, left, right):
        return Node(node_type="operator", value=op_type, left=left, right=right)
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if token == "(":
            stack.append(token)
        elif token == ")":
            right = stack.pop()
            operator = stack.pop()
            left = stack.pop()
            stack.pop() 
            stack.append(create_node(operator, left, right))
        elif token in ["AND", "OR"]:
            stack.append(token)
        else:
            stack.append(Node(node_type="operand", value=token))
        
        i += 1
    
    return stack[0]  

