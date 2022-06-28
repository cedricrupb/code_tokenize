
from ..config    import TokenizationConfig

from .python import create_tokenization_config as pytok_config
from .java   import create_tokenization_config as jvtok_config
from .go     import create_tokenization_config as gotok_config
from .js     import create_tokenization_config as jstok_config
from .php    import create_tokenization_config as phptok_config
from .ruby   import create_tokenization_config as rubytok_config


def load_from_lang_config(lang, **kwargs):
    
    if lang == "python"       : base_config = pytok_config()
    elif lang == "java"       : base_config = jvtok_config()
    elif lang == "go"         : base_config = gotok_config()
    elif lang == "javascript" : base_config = jstok_config()
    elif lang == "php"        : base_config = phptok_config()
    elif lang == "ruby"       : base_config = rubytok_config()
    else                      : base_config = TokenizationConfig(lang)

    base_config.update(kwargs)
    return base_config
