from utils.create_node import Node
def combine_rules(asts, operator):
    if not asts:
        return None
    if len(asts) == 1:
        return asts[0]
    
    combined_ast = asts[0]
    for ast in asts[1:]:
        combined_ast = Node(node_type="operator", value=operator, left=combined_ast, right=ast)
    
    return combined_ast

from utils.create_node import Node

def collect_unique_operands(node, seen_operands=None):
    """Collects unique operands from the AST, avoiding duplicates."""
    if node is None:
        return set()

    if seen_operands is None:
        seen_operands = set()

    if node.node_type == "operand" and node.value not in seen_operands:
        seen_operands.add(node.value)

    if node.left:
        collect_unique_operands(node.left, seen_operands)
    if node.right:
        collect_unique_operands(node.right, seen_operands)

    return seen_operands

def build_ast_from_operands(operands, operator):

    if not operands:
        return None

    combined_ast = Node(node_type="operand", value=operands[0])
    for operand in operands[1:]:
        operand_node = Node(node_type="operand", value=operand)
        combined_ast = Node(node_type="operator", value=operator, left=combined_ast, right=operand_node)

    return combined_ast

def combine_rules(asts, operator):
    if not asts:
        return None

    unique_operands = set()
    for ast in asts:
        unique_operands.update(collect_unique_operands(ast))

    return build_ast_from_operands(list(unique_operands), operator)

