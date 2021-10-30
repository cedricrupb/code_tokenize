
from .parsers import ASTParser
from .config  import TokenizationConfig
from .tokens  import tokenize_tree

# Main function --------------------------------

def tokenize(source_code, lang = "python", **kwargs):

    # Setup config
    config = TokenizationConfig(lang, **kwargs)

    # Parse source tree
    parser = ASTParser(config.lang)
    tree, code = parser.parse(source_code)

    return tokenize_tree(tree.root_node, code)



# -----------------------------------------------