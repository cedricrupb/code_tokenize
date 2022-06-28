from ...config import TokenizationConfig

# Tokenization config ----------------------------------------------------------------

def create_tokenization_config():
    return TokenizationConfig(
        lang = 'php',
        statement_types = ["*_statement"],
        indent_tokens   = False
    )