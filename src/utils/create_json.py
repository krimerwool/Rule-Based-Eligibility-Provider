import json
import os 
from utils.create_node import Node
def ast_to_dict(node):
    if node is None:
        return None
    return {
        "type": node.node_type,
        "value": node.value,
        "left": ast_to_dict(node.left),
        "right": ast_to_dict(node.right)
    }



def dict_to_ast(d):
    if d is None:
        return None
    return Node(node_type=d['type'], value=d['value'], left=dict_to_ast(d['left']), right=dict_to_ast(d['right']))



def save_ast_to_json(ast, file_path):
    ast_dict = ast_to_dict(ast)

    try:
        with open(file_path, 'w') as json_file:
            json.dump(ast_dict, json_file, indent=4)
        print(f"AST saved to '{file_path}' successfully.")
    except Exception as e:
        print(f"An error occurred while saving AST to JSON: {str(e)}")


def load_ast_from_json(file_path = r'files\ast_dict.json'):
    """Load the AST from a JSON file and convert it back to a Node-based AST."""
    try:
        with open(file_path, 'r') as json_file:
            ast_dict = json.load(json_file)
        ast = dict_to_ast(ast_dict)
        print(f"AST loaded successfully from '{file_path}'.")
        return ast
    except FileNotFoundError:
        print(f"File '{file_path}' does not exist.")
        return None
    except json.JSONDecodeError:
        print(f"File '{file_path}' is not a valid JSON file.")
        return None
    except Exception as e:
        print(f"An error occurred while loading AST from JSON: {str(e)}")
        return None



