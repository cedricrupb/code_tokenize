
from functools import lru_cache
from tree_sitter import Language, Parser


# Ultimately replace with AutoLoading --------------------------------

PATH_TO_LANG = 'build/python-language.so'

Language.build_library(
  PATH_TO_LANG,
  [
    'build/tree-sitter-python'
  ]
)


@lru_cache
def load_language(lang):
    """Load Tree Sitter language (cached)"""

    if lang == 'python': return Language(PATH_TO_LANG, 'python')

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

def traverse_tree(root_node):

    queue = [root_node]
    while len(queue) > 0:
        node = queue.pop(0)

        if node.type == "string":
            yield node
            continue

        for child in node.children:
            queue.append(child)

        if not node.children:
            yield node 


def match_span(source_tree, source_lines):
    
    start_line, start_char = source_tree.start_point
    end_line,   end_char   = source_tree.end_point

    assert start_line <= end_line
    assert start_line != end_line or start_char < end_char

    source_area     = source_lines[start_line:end_line + 1]
    
    if start_line == end_line:
        source_area[0] = source_area[0][start_char:end_char]
    else:
        source_area[0]  = source_area[0][start_char:]
        source_area[-1] = source_area[-1][:end_char]

    return "\n".join(source_area)
