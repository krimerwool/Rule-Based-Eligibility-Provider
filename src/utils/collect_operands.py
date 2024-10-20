def collect_operands(node):
    if node is None:
        return []

    if node.node_type == "operand":
        return [node.value]

    left_operands = collect_operands(node.left)
    right_operands = collect_operands(node.right)

    return left_operands + right_operands


import re

import re


def collect_operands_for_user_data(node, memo=None):
    """Collects attribute names from the AST for collecting user data, using dynamic programming."""
    if node is None:
        return []
    if memo is None:
        memo = {}

    if node in memo:
        return memo[node]

    if node.node_type == "operand":
        match = re.match(r'(\w+)\s*[><=]', node.value)
        if match:
            memo[node] = [match.group(1)]
            return memo[node]
        match = re.match(r'(\w+)\s*=', node.value)
        if match:
            memo[node] = [match.group(1)]
            return memo[node]
    left_operands = collect_operands_for_user_data(node.left, memo)
    right_operands = collect_operands_for_user_data(node.right, memo)

    result = list(set(left_operands + right_operands))
    memo[node] = result
    return result

