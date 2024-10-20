
from logic.parsing import parse_condition, parse_expression
def evaluate_condition(node, data):
    return parse_condition(node.value)(data)

def evaluate_ast(node, data):
    if node.node_type == "operand":
        return evaluate_condition(node, data)
    
    left_result = evaluate_ast(node.left, data)
    right_result = evaluate_ast(node.right, data)
    
    if node.value == "AND":
        return left_result and right_result
    elif node.value == "OR":
        return left_result or right_result

