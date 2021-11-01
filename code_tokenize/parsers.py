
from functools import lru_cache
from tree_sitter import Language, Parser


# Ultimately replace with AutoLoading --------------------------------

PATH_TO_LANG = 'build/misc-language.so'

Language.build_library(
  PATH_TO_LANG,
  [
    'build/tree-sitter-python',
    'build/tree-sitter-java'
  ]
)


@lru_cache
def load_language(lang):
    """Load Tree Sitter language (cached)"""

    if lang == 'python': return Language(PATH_TO_LANG, 'python')
    if lang == 'java':   return Language(PATH_TO_LANG, 'java')

    raise ValueError("No available language parse for %s" % lang)

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
