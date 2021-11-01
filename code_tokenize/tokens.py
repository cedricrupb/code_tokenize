from .parsers import match_span


# Tokens -------------------------------------------------------------------


class Token:

    def __init__(self, config, ast_node, source_lines):
        self.config = config
        self.ast_node = ast_node
        self.source_lines = source_lines
        self.root_sequence = None

        self._cache = {}

    # The sequence of tokens is static. Therefore, we can cache computed results
    def cached_property(fnc):
        name = fnc.__name__
        def load_from_cache(self):
            if name not in self._cache:
                self._cache[name] = fnc(self)
            return self._cache[name]

        return property(load_from_cache)
    
    def _create_token(self, node):
        if self.root_sequence is not None:
            return self.root_sequence.get_token_by_node(node)
        return Token(self.config, node, self.source_lines)

    def __repr__(self):
        return self.text

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




# Token Collection -----------------------------------------------------

class TokenSequence(list):

    def __init__(self, tokens):
        super().__init__(tokens)

        self._map_nodes = {}

        for tok in self:
            tok.root_sequence = self
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
