from code_ast import ASTVisitor

# Basic visitor -----------------------------------------------------------

class LeafVisitor(ASTVisitor):

    def __init__(self, node_handler):
        self.node_handler = node_handler

    def visit_string(self, node):
        self.node_handler(node)
        return False

    def visit(self, node):
        if node.child_count == 0:
            self.node_handler(node)
            return False