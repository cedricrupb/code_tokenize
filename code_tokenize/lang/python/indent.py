"""Hierarchical indentation independent of the concrete program formatting"""

from code_ast.visitor import ASTVisitor
from ...tokens  import IndentToken, DedentToken, NewlineToken


class IndentVisitor(ASTVisitor):

    def __init__(self, token_handler):
        super().__init__()
        self.config = token_handler.config
        self.handler = token_handler

    def visit_block(self, block):
        self.handler.handle_token(IndentToken(self.config))

    def leave_block(self, block):
        self.handler.handle_token(DedentToken(self.config))

    def leave_comment(self, comment):
        self.handler.handle_token(NewlineToken(self.config))

    def leave(self, node):
        if not node.type.endswith('statement'): return
        self.handler.handle_token(NewlineToken(self.config))