from ...config import TokenizationConfig

# Tokenization config ----------------------------------------------------------------

def create_tokenization_config():
    return TokenizationConfig(
        lang = 'ruby',
        statement_types = ["*_statement"],
        indent_tokens   = True
    )