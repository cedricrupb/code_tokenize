from . import tokens as T
from .tokens  import ASTToken, TokenSequence
from .parsers import traverse_tree

import logging as logger

# Tokenize ----------------------------------------------------------------

class BaseTokenizer:
    
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

    def __init__(self, config, pre_transform = None, post_transform = None):
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



def create_tokenizer(config):

    pre_transform, post_transform = None, None

    if config.ident_tokens:
        post_transform = insert_indent_tokens

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

# Interface ----------------------------------------------------------------

def tokenize_tree(config, code_tree, code_lines):
    return create_tokenizer(config)(code_tree, code_lines)
