
from ...config import TokenizationConfig

# Tokenization config ----------------------------------------------------------------

def create_tokenization_config():
    return TokenizationConfig(
        lang = 'go',
        statement_types = ["*_statement", "*_declaration"],
        indent_tokens   = False
    )