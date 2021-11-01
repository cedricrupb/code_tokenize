
class TokenizationConfig:

    def __init__(self, lang, **kwargs):
        self.lang = lang

        # A list of all statement node defined in the language
        self.statement_types = [
            "*_statement", "*_definition", "*_declaration"
        ]

    
    def update(self, kwargs):
        for k, v in kwargs.iteritems():

            if k not in self.__dict__:
                raise TypeError("TypeError: tokenize() got an unexpected keyword argument '%s'" % k)
        
            self.__dict__[k] = v

