
from ..config import TokenizationConfig

from .python import create_tokenization_config as pytok_config
from .java   import create_tokenization_config as jvtok_config


def load_from_lang_config(lang, **kwargs):
    
    if lang == "python" : base_config = pytok_config()
    elif lang == "java" : base_config = jvtok_config()
    else                : base_config = TokenizationConfig(lang)

    base_config.update(kwargs)
    return base_config