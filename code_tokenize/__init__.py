
from .parsers import ASTParser
from .config  import load_from_lang_config
from .tokenizer import tokenize_tree

import logging as logger

# Main function --------------------------------

def tokenize(source_code, lang = "guess", **kwargs):
    """
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

    # If lang == guess, automatically determine the language
    if lang == "guess": lang = _lang_detect(source_code)

    logger.debug("Parses source code with parser for %s" % lang)

    # Setup config
    config = load_from_lang_config(lang, **kwargs)

    # Parse source tree
    parser = ASTParser(config.lang)
    tree, code = parser.parse(source_code)
    
    return tokenize_tree(config, tree.root_node, code)



# Lang detect --------------------------------------  


def _lang_detect(source_code):
    """Guesses the source code type using pygments"""
    raise NotImplementedError(
        "Guessing the language automatically is currently not implemented. Please specify a language with the lang keyword\n code_tokenize.tokenize(code, lang = your_lang)"
    )

