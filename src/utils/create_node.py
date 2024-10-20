class Node:
    def __init__(self, node_type, value, left=None, right=None):
        self.node_type = node_type
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        left = f"Left({self.left})" if self.left else "None"
        right = f"Right({self.right})" if self.right else "None"
        return f"Node(type={self.node_type}, value={self.value}, {left}, {right})"



