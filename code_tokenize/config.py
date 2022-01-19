import os
import json


class TokenizationConfig:
    """Helper object to translate arguments of tokenize to config object"""

    def __init__(self, lang, **kwargs):
        self.lang = lang
        self.syntax_error = "raise" # Options: raise, warn, ignore

        self.ident_tokens = False # Whether to represent indentations and newlines (Helpful for script languages like Python)

        # A list of all statement node defined in the language
        self.statement_types = [
            "*_statement", "*_definition", "*_declaration"
        ]

        self.path_handler = None # A dictionary that maps path handler to AST node types

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


def _get_config_path():
    current_path = os.path.abspath(__file__)

    while len(current_path) > 0 and os.path.basename(current_path) != "code_tokenize":
        current_path = os.path.dirname(current_path)
    parent_path = os.path.dirname(current_path)

    return os.path.join(parent_path, "lang_configs")


def load_from_lang_config(lang, **kwargs):
    """Automatically bootstrap config from language specific config"""
    config_path = _get_config_path()
    config_path = os.path.join(config_path, "%s.json" % lang)

    if os.path.exists(config_path):
        kwargs["lang"] = lang
        return load_from_config(config_path, **kwargs)

    return TokenizationConfig(lang, **kwargs)


