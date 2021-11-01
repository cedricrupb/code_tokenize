
import os
from tree_sitter import Language, Parser

import logging as logger

# For autoloading
import requests
from git import Repo


# Automatic loading of Tree-Sitter parsers --------------------------------

def load_language(lang):

    cache_path = _path_to_local()
    
    compiled_lang_path = os.path.join(cache_path, "%s-lang.so" % lang)
    source_lang_path   = os.path.join(cache_path, "tree-sitter-%s" % lang)

    if os.path.isfile(compiled_lang_path):
        return Language(compiled_lang_path, lang)
    
    if os.path.exists(source_lang_path) and os.path.isdir(source_lang_path):
        logger.warn("Compiling language for %s" % lang)
        _compile_lang(source_lang_path, compiled_lang_path)
        return load_language(lang)

    logger.warn("Autoloading AST parser for %s: Start download from Github." % lang)
    _clone_parse_def_from_github(lang, source_lang_path)
    return load_language(lang)

# Parser ---------------------------------------------------------------

class ASTParser:

    def __init__(self, lang):
        self.lang_id = lang
        self.lang    = load_language(lang)
        self.parser  = Parser()
        self.parser.set_language(self.lang)

    def parse_bytes(self, data):
        return self.parser.parse(data)

    def parse(self, source_code):
        source_lines = source_code.splitlines()
        source_bytes = source_code.encode("utf-8")

        return self.parse_bytes(source_bytes), source_lines


# Utils ------------------------------------------------

def _traverse_tree(root_node, stop_fn = None):

    if stop_fn is None: stop_fn = lambda x: False

    stack = [root_node]
    while len(stack) > 0:
        node = stack.pop(-1)

        if node.type == "string":
            yield node
            continue

        for child in node.children:
            if stop_fn(child): continue
            stack.append(child)

        if not node.children:
            yield node 

def traverse_tree(root_node, stop_fn = None):
    return list(_traverse_tree(root_node, stop_fn))[::-1]


def match_span(source_tree, source_lines):
    
    start_line, start_char = source_tree.start_point
    end_line,   end_char   = source_tree.end_point

    assert start_line <= end_line
    assert start_line != end_line or start_char <= end_char

    source_area     = source_lines[start_line:end_line + 1]
    
    if start_line == end_line:
        return source_area[0][start_char:end_char]
    else:
        source_area[0]  = source_area[0][start_char:]
        source_area[-1] = source_area[-1][:end_char]
        return "\n".join(source_area)


# Auto Load Languages --------------------------------------------------

PATH_TO_LOCALCACHE = None

def _path_to_local():
    global PATH_TO_LOCALCACHE
    
    if PATH_TO_LOCALCACHE is None:
        current_path = os.path.abspath(__file__)
        
        while os.path.basename(current_path) != "code_tokenize":
            current_path = os.path.dirname(current_path)
        
        current_path = os.path.dirname(current_path) # Top dir
        PATH_TO_LOCALCACHE = os.path.join(current_path, "build")
        
    return PATH_TO_LOCALCACHE


def _compile_lang(source_path, compiled_path):
    logger.debug("Compile language from %s" % compiled_path)

    Language.build_library(
        compiled_path,
        [
            source_path
        ]
    )


# Auto Clone from Github --------------------------------
    
def _exists_url(url):
    req = requests.get(url)
    return req.status_code == 200


def _clone_parse_def_from_github(lang, cache_path):
    
    # Start by testing whethe repository exists
    REPO_URL = "https://github.com/tree-sitter/tree-sitter-%s" % lang

    if not _exists_url(REPO_URL):
        raise ValueError("There is no parsing def for language %s available." % lang)

    logger.warn("Start cloning the parser definition from Github.")
    try:  
        Repo.clone_from(REPO_URL, cache_path)
    except Exception:
        raise ValueError("To autoload a parsing definition, git needs to be installed on the system!")








