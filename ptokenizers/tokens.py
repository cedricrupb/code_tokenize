from .parsers import traverse_tree, match_span

# Tokenize ----------------------------------------------------------------

def tokenize_tree(code_tree, code_lines):
    return [Token(node, code_lines) for node in traverse_tree(code_tree)]


# Tokens -------------------------------------------------------------------

class Token:

    def __init__(self, token_node, source_lines):
        self.token_node = token_node
        self.source_lines = source_lines

        self._text = None

    @property
    def text(self):
        if self._text is None:
            self._text = match_span(self.token_node, self.source_lines)
        return self._text

    def __repr__(self):
        return self.text




