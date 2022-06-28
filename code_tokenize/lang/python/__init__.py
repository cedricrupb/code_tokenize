
from ...config import TokenizationConfig

from ..base_visitors import LeafVisitor
from .indent         import IndentVisitor


# Tokenization config ----------------------------------------------------------------

def create_tokenization_config():
    return TokenizationConfig(
        lang = "python",
        statement_types = ["*_statement", "*_definition"],
        visitors = [PythonLeafVisitor, IndentVisitor],
        indent_tokens   = True
    )

# Custom leaf visitor ----------------------------------------------------------------

class PythonLeafVisitor(LeafVisitor):

   def visit_unary_operator(self, node):
        if node.children[-1].type == "integer":
            self.node_handler(node)
            return False