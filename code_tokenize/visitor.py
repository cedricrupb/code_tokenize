from pydoc import visiblename
from .parsers import ASTParser
from .config  import load_from_lang_config

from .tokens  import ASTToken, TokenSequence
from .tokens  import IndentToken, DedentToken, NewlineToken

from .tokenizer import warn_syntax_error, raise_syntax_error

import logging as logger

# Experimental ----------------------------------------------------------------

def tokenize(source_code, lang = "guess", **kwargs):
    """
    Experimental implementation: Use visitor to process AST tree instead of specific parser

    Tokenizes source code of most programming languages quickly.

    Given source code as string, this function quickly tokenizes
    the code into basic program tokens. 
    The function uses tree-sitter as a backend. Therefore, this
    function does not only support most programming languages (see README)
    but also relates every token to an AST node.
    Tokens can be abused to traverse the program AST.

    Parameters
    ----------
    source_code : str
        Source code to parsed as a string. Also
        supports parsing of incomplete source code
        snippets (by deactivating the syntax checker; see syntax_error)
    
    lang : [python, java, javascript, ...]
        String identifier of the programming language
        to be parsed. Supported are most programming languages
        including python, java and javascript (see README)
        Default: guess (Guesses language / Not supported currently throws error currently)
    
    syntax_error : [raise, warn, ignore]
        Reaction to syntax error in code snippet.
        raise:  raises a Syntax Error
        warn:   prints a warning to console
        ignore: Ignores syntax errors. Helpful for parsing code snippets.
        Default: raise

    Returns
    -------
    TokenSequence
        A list of tokens representing the source code snippet.
    
    """

    if len(source_code.strip()) == 0: raise ValueError("The code string is empty. Cannot tokenize anything empty: %s" % source_code) 

    if lang == "guess": raise NotImplementedError()

    logger.debug("Parses source code with parser for %s" % lang)

    # Setup config
    config = load_from_lang_config(lang, **kwargs)

    # Parse source tree
    parser = ASTParser(config.lang)
    tree, code = parser.parse(source_code)
    
    return tokenize_tree(config, tree.root_node, code)


# ----------------------------------------------------------------------------


class ASTVisitor:

    # Decreased version of visit (no edges are supported) -----------------------

    def visit(self, node):
        # Default handler: Override to capture all nodes
        return True

    def _visit(self, node):
        if self.visit(node) is False: return False

        visitor_fn = getattr(self, "visit_%s" % node.type, None)
        return visitor_fn is None or visitor_fn(node) is not False

    # Navigation ----------------------------------------------------------------

    def walk(self, root_node):
        cursor   = root_node.walk()
        has_next = True

        while has_next:
            current_node = cursor.node
            # Step 1: Try to go to next child if we continue the subtree
            if self._visit(current_node):
                has_next = cursor.goto_first_child()
            else:
                has_next = False

            # Step 2: Stop if parent or sibling is out of subtree
            if not has_next and node_equal(current_node, root_node):
                break

            # Step 3: Try to go to next sibling
            if not has_next:
                has_next = cursor.goto_next_sibling()

            previous_node = current_node

            # Step 4: Go up until sibling exists
            while not has_next and cursor.goto_parent():
                if node_equal(cursor.node, root_node): break
                has_next = cursor.goto_next_sibling()
                has_next = has_next and not node_equal(previous_node, cursor.node)

    def __call__(self, root_node):
        return self.walk(root_node)


# Helper --------------------------------

def node_equal(n1, n2):
    if n1 == n2: return True
    try:
        return (n1.type == n2.type 
                    and n1.start_point == n2.start_point
                    and n1.end_point   == n2.end_point)
    except AttributeError:
        return n1 == n2


# Compositions ----------------------------------------------------------------

class VisitorComposition(ASTVisitor):

    def __init__(self, *visitors):
        super().__init__()
        self.base_visitors = visitors

    def _visit(self, node):
        for base_visitor in self.base_visitors:
            if base_visitor._visit(node) is False: return False
        return True


# Tokenization via visitor ----------------------------------------------------

def tokenize_tree(config, root_node, code):
    handler = IndentHandler(config)
    visitor = BasicTokenizeVisitor(config, code, handler)
    visitor.walk(root_node)
    return handler.tokens()


class TokenHandler:

    def __init__(self):
        self._tokens = []

    def tokens(self):
        return TokenSequence(self._tokens)

    def handle_token(self, token):
        self._tokens.append(token)


class IndentHandler(TokenHandler):

    def __init__(self, config):
        super().__init__()
        self.config = config

        self._last_line   = 0
        self._last_indent = 0

    def handle_token(self, token):
        node = token.ast_node
        start_line, start_char = node.start_point

        if start_line > self._last_line:
            line_indent = start_char // self.config.num_whitespaces_for_indent

            if line_indent > self._last_indent:
                super().handle_token(IndentToken(self.config, new_line_before=True))
            elif line_indent < self._last_indent:
                super().handle_token(DedentToken(self.config, new_line_before = True))
            else:
                super().handle_token(NewlineToken(self.config))

            self._last_line, self._last_indent = start_line, line_indent

        return super().handle_token(token)


class BasicTokenizeVisitor(ASTVisitor):

    def __init__(self, config, source_code, token_handler):
        self.config = config
        self.source_code = source_code
        self.token_handler = token_handler

    def _add_token(self, ast_node):
        self.token_handler.handle_token(ASTToken(self.config, ast_node, self.source_code))

    # ERROR handling --------------------------------------------------------

    def visit_ERROR(self, node):

        if self.config.syntax_error == "raise":
            raise_syntax_error(node)
            return

        if self.config.syntax_error == "warn":
            warn_syntax_error(node)
            return

    # Default node handling --------------------------------------------------

    def visit(self, node):

        if node.type == "string":
            self._add_token(node)
            return False

        if node.child_count == 0:
            self._add_token(node)
            return False

        return True
