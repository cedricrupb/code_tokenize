from . import tokens as T
from .tokens  import ASTToken, TokenSequence
from .parsers import traverse_tree

import logging as logger


# Interface ----------------------------------------------------------------

def tokenize_tree(config, code_tree, code_lines):
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
    return create_tokenizer(config)(code_tree, code_lines)

# Tokenize ----------------------------------------------------------------

class BaseTokenizer:
    """
    Basic tokenizer for parsing AST
    
    The tokenizer parses a given AST into a token sequence. 
    Each token is representing an AST leaf.
    No further analyses or additions.
    """
    
    def __init__(self, config):
        self.config = config

    def preprocess(self, code_tree, code_lines):
        return code_tree, code_lines

    def error_handler(self):
        if self.config.syntax_error == "raise":  return raise_syntax_error
        elif self.config.syntax_error == "warn": return warn_syntax_error
        else:                                    return None

    def tree_tokenize(self, code_tree, code_lines):
        return [ASTToken(self.config, node, code_lines) for node in traverse_tree(code_tree, handle_error=self.error_handler())]

    def postprocess(self, tokens):
        return tokens

    def __call__(self, code_tree, code_lines):
        
        code_tree, code_lines = self.preprocess(code_tree, code_lines)
        tokens = self.tree_tokenize(code_tree, code_lines)
        tokens = self.postprocess(tokens)

        return TokenSequence(tokens)


class PhasedTokenizer(BaseTokenizer):
    """
    Extension of the base tokenizer to support phased analyses

    This tokenizer supports preprocessing of the AST
    tree and post-processing of the token sequence.
    
    """

    def __init__(self, config, pre_transform = None, post_transform = None):
        """
        Initializes the phased tokenizer

        Parameters
        ----------
        config : TokenizationConfig
            configuration to guide the tokenization process

        pre_transform : fn root_node, source_lines -> root_node, source_lines
            Function to preprocess the given AST before tokenization
            Default: None (No preprocessing)

        post_transform : fn list[Token] -> list[Token]
            Function to postprocess the produced token sequence
            Default: None (No postprocessing)
    
        """
        super().__init__(config)
        self.pre_transform = pre_transform
        self.post_transform = post_transform

    def preprocess(self, code_tree, code_lines):
        if self.pre_transform:
            code_tree, code_lines = self.pre_transform(code_tree, code_lines)
        return super().preprocess(code_tree, code_lines)

    def postprocess(self, tokens):
        tokens = super().postprocess(tokens)

        if self.post_transform:
            return self.post_transform(tokens)
        
        return tokens


class PathTokenizer(PhasedTokenizer):
    """
    AST path based code tokenizer

    The tokenization process is dependent on the AST path
    leading to the leaf node / token.

    """

    def __init__(self, config, handler, **kwargs):
        """
        Initializes the path tokenizer

        Parameters
        ----------
        config : TokenizationConfig
            configuration to guide the tokenization process

        handler : dict[str, Tokenizer]
            Maps a path key to a handler function
            Handler function should map a leaf node to a program token

        pre_transform : fn root_node, source_lines -> root_node, source_lines
            Function to preprocess the given AST before tokenization
            Default: None (No preprocessing)

        post_transform : fn list[Token] -> list[Token]
            Function to postprocess the produced token sequence
            Default: None (No postprocessing)
    
        """
        super().__init__(config, **kwargs)
        self.handler = handler

        self.path_keys = {}
        for handler_type, keys in config.path_handler.items():
            for key in keys:
                node_type, edge_type = key.rsplit("_", 1)
                if node_type not in self.path_keys:
                    self.path_keys[node_type] = {}
                assert edge_type not in self.path_keys[node_type]
                self.path_keys[node_type][edge_type] = handler_type

    
    def _find_handler(self, node, path_handler_cache):
        # Track path to root / Stop if handler found
        node_handler = "ast"

        current_node = node
        while current_node.parent is not None:
            current_key = T.node_key(current_node)
            if current_key in path_handler_cache:
                node_handler = path_handler_cache[current_key]
                break

            # typ_edge means that we look at the parent relation
            parent_node = current_node.parent
            parent_node_type = parent_node.type
            if parent_node_type not in self.path_keys: 
                current_node = parent_node
                continue

            for edge_type, handler in self.path_keys[parent_node_type].items():

                if edge_type == "*":
                    match = True
                else:
                    named_children = parent_node.child_by_field_name(edge_type)
                    match = named_children == current_node

                if match:
                    node_handler = handler
                    break

            if node_handler != "ast":
                path_handler_cache[current_key] = node_handler
                break
            else:
                current_node = parent_node
        
        return node_handler


    def tree_tokenize(self, code_tree, code_lines):
        path_handler_cache = {}

        tokens = []
        for leaf_node in traverse_tree(code_tree, handle_error = self.error_handler()):
            node_handler = self._find_handler(leaf_node, path_handler_cache)
            if node_handler not in self.handler: node_handler = "ast"
            token = self.handler[node_handler](self.config, leaf_node, code_lines)
            
            tokens.append(token)

        return tokens



def create_tokenizer(config):
    """Function to create tokenizer based on configuration"""

    pre_transform, post_transform = None, None

    if config.ident_tokens:
        post_transform = insert_indent_tokens
    
    if config.path_handler:
        return PathTokenizer(config, get_node_type_handler_index(),
                pre_transform = pre_transform, post_transform = post_transform)

    if pre_transform or post_transform:
        return PhasedTokenizer(config, pre_transform, post_transform)
    return BaseTokenizer(config)


# Transforms -----------------------------------------------------------


def insert_indent_tokens(tokens):
    last_line  = 0
    last_indent = 0

    indent_tokens = []
    for token in tokens:
        start_line, start_char = token.ast_node.start_point
        
        if start_line > last_line:
            line_indent = start_char // 4 # Assume ident with 4 spaces
            
            if line_indent > last_indent:
                indent_tokens.append(T.IndentToken(token.config, new_line_before=True))
            elif line_indent < last_indent:
                indent_tokens.append(T.DedentToken(token.config, new_line_before = True))
            else:
                indent_tokens.append(T.NewlineToken(token.config))
            
            last_line, last_indent = start_line, line_indent
        
        indent_tokens.append(token)

    return indent_tokens


# Node type handler --------------------------------------------------------

def get_node_type_handler_index():
    return {
        "var_def": vardef_handler,
        "var_use": varuse_handler,
        "ast": default_handler
    }


def default_handler(config, leaf_node, code_lines):
    return ASTToken(config, leaf_node, code_lines)


def vardef_handler(config, leaf_node, code_lines):

    if leaf_node.type != "identifier":
        return default_handler(config, leaf_node, code_lines)

    return T.VarDefToken(config, leaf_node, code_lines)


def varuse_handler(config, leaf_node, code_lines):

    if leaf_node.type != "identifier":
        return default_handler(config, leaf_node, code_lines)

    return T.VarUseToken(config, leaf_node, code_lines)



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
