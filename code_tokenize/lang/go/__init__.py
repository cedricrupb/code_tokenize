
from ...config import TokenizationConfig
from ...tokens import NewlineToken

from ..base_visitors import LeafVisitor


# Tokenization config ----------------------------------------------------------------

def create_tokenization_config():
    return TokenizationConfig(
        lang = 'go',
        statement_types = ["*_statement", "*_declaration"],
        visitors = [GoLeafVisitor],
        indent_tokens   = False
    )

# Custom leaf visitor ----------------------------------------------------------------

class GoLeafVisitor(LeafVisitor):

    def visit_interpreted_string_literal(self, node):
        self.node_handler(node)
        return False

    def visit(self, node):
        if node.type == "\n":
            self.node_handler.handle_token(NewlineToken(self.node_handler.config))
            return False
        return super().visit(node)