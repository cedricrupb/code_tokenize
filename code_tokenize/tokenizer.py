
import logging as logger
from code_ast.visitor import ASTVisitor, ResumingVisitorComposition

from .tokens  import ASTToken, TokenSequence


# Interface ----------------------------------------------------------------

def tokenize_tree(config, code_tree, code_lines, visitors = None):
    """
    Transforms AST tree into token sequence

    Function to analyse an AST tree resulting
    into a token sequence. The parsing process
    is fully customizable and is guided by the given
    configuration.
    Tokenizers also support additional analysis
    of AST tree and extenstions to the token sequence.

    Parameters
    ----------
    config : TokenizationConfig
        A configuration which used to initialize the tokenizers

    code_tree: tree-sitter root node
        Root node of the program to be tokenized
    
    code_lines: list[str]
        Source lines of the program code to be tokenized.
        Has to be related to code_tree. Otherwise, behavior
        is undefined.

    Returns
    -------
    TokenSequence
        A sequence of program tokens representing the given program

    """
    return create_tokenizer(config)(code_tree, code_lines, visitors = visitors)


# Tokenize ----------------------------------------------------------------


class Tokenizer:
    """
    Basic tokenizer for parsing AST
    
    The tokenizer parses a given AST into a token sequence. 
    Each token is representing an AST leaf.
    No further analyses or additions.
    """
    
    def __init__(self, config):
        self.config    = config
        self._visitor_factories = []

    def append_visitor(self, visitor_factory):
        self._visitor_factories.append(visitor_factory)

    def _create_token_handler(self, code_lines):
        return TokenHandler(self.config, code_lines)

    def _create_tree_visitors(self, token_handler, visitors = None):
        visitors  = visitors or []
        visitors += self._visitor_factories

        visitors  = [visitor_fn(token_handler) 
                        if callable(visitor_fn) 
                            else visitor_fn
                        for visitor_fn in visitors]

        return ResumingVisitorComposition(
            ErrorVisitor(self.config),
            *visitors
        )

    def __call__(self, code_tree, code_lines, visitors = None):
        token_handler = self._create_token_handler(code_lines)
        tree_visitor  = self._create_tree_visitors(token_handler, visitors)

        # Run tree visitor
        tree_visitor.walk(code_tree)

        return token_handler.tokens()


def create_tokenizer(config):
    """Function to create tokenizer based on configuration"""
    return Tokenizer(config)


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


class ErrorVisitor(ASTVisitor):

    def __init__(self, config):
        self.config = config

    def visit_ERROR(self, node):

        if self.config.syntax_error == "raise":
            raise_syntax_error(node)
            return

        if self.config.syntax_error == "warn":
            warn_syntax_error(node)
            return

# Node handler ------------------------------------------------------------

class TokenHandler:

    def __init__(self, config, source_code):
        self.config = config
        self.source_code = source_code

        self._tokens = []

    def tokens(self):
        result = TokenSequence(self._tokens)
        self._tokens = []
        return result
    
    def handle_token(self, token):
        if token.type == "newline" and self._tokens[-1].type in ["indent", "dedent", "newline"]:
            return # TODO: Blocking double newlines seems to be general. Better solution?

        self._tokens.append(token)

    def __call__(self, node):
        self.handle_token(
            ASTToken(self.config, node, self.source_code)
        )

# Error handling -----------------------------------------------------------

def _construct_error_msg(node):

    start_line, start_char = node.start_point
    end_line, end_char     = node.end_point

    position = "?"
    if start_line == end_line:
        position = "in line %d [pos. %d - %d]" % (start_line, start_char, end_char)
    else:
        position = "inbetween line %d (start: %d) to line %d (end: %d)" % (start_line, start_char, end_line, end_char)

    return "Problem while parsing given code snipet. Error occured %s" % position


def warn_syntax_error(node):
    logger.warn(_construct_error_msg(node))


def raise_syntax_error(node):
    raise SyntaxError(_construct_error_msg(node))
