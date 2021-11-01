
from .parsers import ASTParser
from .config  import TokenizationConfig
from .tokenizer import tokenize_tree

import logging as logger

# Main function --------------------------------

def tokenize(source_code, lang = "guess", **kwargs):

    # If lang == guess, automatically determine the language
    if lang == "guess": lang = lang_detect(source_code)

    logger.debug("Parses source code with parser for %s" % lang)

    # Setup config
    config = TokenizationConfig(lang, **kwargs)

    # Parse source tree
    parser = ASTParser(config.lang)
    tree, code = parser.parse(source_code)

    return tokenize_tree(config, tree.root_node, code)



# Lang detect --------------------------------------  


def lang_detect(source_code):
    """Guesses the source code type using pygments"""
    raise NotImplementedError(
        "Guessing the language automatically is currently not implemented. Please specify a language with the lang keyword\n code_tokenize.tokenize(code, lang = your_lang)"
    )

