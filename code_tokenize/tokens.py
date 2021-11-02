from .parsers import match_span

# Cache Properties ---------------------------------------------------------

def cached_property(fnc):
    name = fnc.__name__

    def get_or_compute(self):
        cache_attr = getattr(self, "_%s" % name, None)
        if cache_attr is not None: return cache_attr
        
        if not hasattr(self, "_cache"): self._cache = {}

        if name not in self._cache:
            self._cache[name] = fnc(self)
        
        return self._cache[name]
    
    return property(get_or_compute)


# Tokens -------------------------------------------------------------------

class Token:

    def __init__(self, config, text):
        """Representing a single program token"""
        self.config = config
        self._text   = text
        self._type   = "token"

        self.root_sequence = None

    @property
    def text(self):
        return self._text

    @property
    def type(self):
        return self._type

    def __repr__(self):
        return self.text


class IndentToken(Token):

    def __init__(self, config, new_line_before = True):
        super().__init__(config, "#INDENT#")
        self.new_line_before = new_line_before
        self._type = "indent"
        

class DedentToken(Token):

    def __init__(self, config, new_line_before = True):
        super().__init__(config, "#DEDENT#")
        self.new_line_before = new_line_before
        self._type = "dedent"


class NewlineToken(Token):

    def __init__(self, config):
        super().__init__(config, "#NEWLINE#")
        self._type = "newline"


# AST backed token  ----------------------------------------------------------------

class ASTToken(Token):

    def __init__(self, config, ast_node, source_lines):
        super().__init__(config, None)
        self.ast_node = ast_node
        self.source_lines = source_lines
        self.root_sequence = None
    
    def _create_token(self, node):
        if self.root_sequence is not None:
            return self.root_sequence.get_token_by_node(node)
        return ASTToken(self.config, node, self.source_lines)

    # API methods --------------------------------

    @cached_property
    def text(self):
        return match_span(self.ast_node, self.source_lines)

    @property
    def type(self):
        return self.ast_node.type

    @cached_property
    def statement_head(self):
        """Returns the token representing the head of a statement"""

        statement_types = self.config.statement_types
        
        parent_node = parent_statement_node(statement_types, self.ast_node)
        if parent_node is None: raise ValueError("No statement could be identified!")

        # Identify first token that belongs to the statement
        current_left = parent_node
        while not is_token(current_left):
            current_left = current_left.children[0]

        return self._create_token(current_left)

    @cached_property
    def parent_head(self):
        """
        Returns head of parent node if it exists.

        If the current token belongs to a top level statement,
        the function return None.
        """
        # For identifying statements
        statement_types = self.config.statement_types
        parent_node     = parent_statement_node(statement_types, self.ast_node)
        if parent_node is None: raise ValueError("No statement could be identified!")

        grandparent_node = parent_statement_node(statement_types, parent_node)
        if grandparent_node is None: return None

        # Identify first token that belongs to the statement
        current_left = grandparent_node
        while not is_token(current_left):
            current_left = current_left.children[0]

        return self._create_token(current_left)


class VariableToken(ASTToken):

    def __init__(self, config, ast_node, source_lines, is_use = False):
        super().__init__(config, ast_node, source_lines)
        self.is_use = is_use
        self._type  = "use_var" if is_use else "def_var"



# Token Collection -----------------------------------------------------

class TokenSequence(list):

    def __init__(self, tokens):
        super().__init__(tokens)

        self._map_nodes = {}

        for tok in self:
            tok.root_sequence = self

            if hasattr(tok, "ast_node"):
                self._map_nodes[node_key(tok.ast_node)] = tok

    def get_token_by_node(self, node):
        return self._map_nodes[node_key(node)]

    def iterstmts(self):
        def _iter_stmts():
            current_head = None
            stmt = []

            for tok in self:
                tok_head = tok.statement_head

                if tok_head != current_head:
                    if len(stmt) > 0: yield stmt
                    current_head = tok_head
                    stmt = []

                stmt.append(tok)
            
            if len(stmt) > 0: yield stmt

        return _iter_stmts()


# Utils ----------------------------------------------------------------

def match_type(type_regex, type):
    # TODO Support general regex (Is this needed?)

    star_count = type_regex.count("*")

    if star_count == 0:
        return type == type_regex

    if  star_count == 1:
        if type_regex[0] == "*":
            return type.endswith(type_regex[1:])
        if type_regex[-1] == "*":
            return type.startswith(type_regex[:-1])

    raise ValueError("Unsupported type regex: %s" % type_regex)


def is_token(node):
    return node.type == "string" or not node.children 


def node_key(node):
    return (node.type, node.start_point, node.end_point)


def parent_statement_node(statement_types, node):

    def is_statement(type):
        return any(match_type(reg, type) for reg in statement_types)
        
    # Go up till we find a statement node
    parent_node = node.parent
    while parent_node is not None and not is_statement(parent_node.type):
        parent_node = parent_node.parent

    return parent_node
