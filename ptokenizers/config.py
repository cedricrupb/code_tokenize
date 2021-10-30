
class TokenizationConfig:

    def __init__(self, lang, **kwargs):
        self.lang = lang

    
    def update(self, kwargs):
        for k, v in kwargs.iteritems():

            if k not in self.__dict__:
                raise TypeError("TypeError: tokenize() got an unexpected keyword argument '%s'" % k)
        
            self.__dict__[k] = v

