
from ...config import TokenizationConfig

# Tokenization config ----------------------------------------------------------------

def create_tokenization_config():
    return TokenizationConfig(
        lang = 'java',
        statement_types = ["*_statement", "*_definition", "*_declaration"],
        indent_tokens   = False
    )
