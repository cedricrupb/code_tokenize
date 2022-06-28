
import json

from .lang.base_visitors import LeafVisitor


class TokenizationConfig:
    """Helper object to translate arguments of tokenize to config object"""

    def __init__(self, lang, **kwargs):
        self.lang = lang
        self.syntax_error = "raise" # Options: raise, warn, ignore

        self.indent_tokens = False # Whether to represent indentations and newlines (Helpful for script languages like Python)
        self.num_whitespaces_for_indent = 4

        # A list of all statement node defined in the language
        self.statement_types = [
            "*_statement", "*_definition", "*_declaration"
        ]

        self.visitors = [LeafVisitor] # visitor classes which should be run during analysis

        self.update(kwargs)

    
    def update(self, kwargs):
        for k, v in kwargs.items():

            if k not in self.__dict__:
                raise TypeError("TypeError: tokenize() got an unexpected keyword argument '%s'" % k)
        
            self.__dict__[k] = v
    
    def __repr__(self):

        elements = []
        for k, v in self.__dict__.items():
            if v is not None:
                elements.append("%s=%s" % (k, v))
        
        return "Config(%s)" % ", ".join(elements)



# From config ----------------------------------------------------------------

def load_from_config(config_path, **kwargs):
    """Load from a config file. Config options can still be overwritten with kwargs"""

    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    config.update(kwargs)

    return TokenizationConfig(**config)

