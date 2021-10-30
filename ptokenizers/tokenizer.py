from .tokens  import Token, TokenSequence
from .parsers import traverse_tree

# Tokenize ----------------------------------------------------------------

class BaseTokenizer:

    def __init__(self, config):
        self.config = config
    
    def __call__(self, code_tree, code_lines):
        return TokenSequence([
                Token(self.config, node, code_lines) 
                for node in traverse_tree(code_tree)]
        )


def create_tokenizer(config):
    return BaseTokenizer(config)


# Interface ----------------------------------------------------------------

def tokenize_tree(config, code_tree, code_lines):
    return create_tokenizer(config)(code_tree, code_lines)
