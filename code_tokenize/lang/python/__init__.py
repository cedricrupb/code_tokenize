
from ...config import TokenizationConfig


# Tokenization config ----------------------------------------------------------------

def create_tokenization_config():
    return TokenizationConfig(
        lang = "python",
        statement_types = ["*_statement", "*_definition"],
        indent_tokens   = True
    )
