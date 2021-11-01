<p align="center">
  <img height="150" src="https://github.com/cedricrupb/ptokenizers/raw/main/resources/code_tokenize.svg" />
</p>

------------------------------------------------

Programminng Language Processing (PLP) brings the capabilities of modern NLP systems to the world of programming languages. 
To achieve high performance PLP systems, existing methods often take advantage of the fully defined nature of programminng languages. Especially the syntactical structure can be exploited to gain knowledge about programs.

Code(dot)tokenize provides easy access to the syntactic structure of a program. The tokenizer converts a program into a sequence of program tokens ready for further end-to-end processing.
By relating each token to an AST node, it is possible to extend the program representation easily with further syntactic information.

## Installation
The package is currently only tested under Python 3. It can be installed via:
````
pip install code_tokenizer
````


## Library highlights
Whether you are on the search for a fast multilingual program tokenizer or want to start your next PLP project, here are some reason why you should build upon ptokenizers:

* **Easy to use** All it takes to tokenize your code is to run a single line:
````
import code_tokenize as ctok

ctok.tokenize(
    '''
        def my_func():
            print("Hello World")
    ''',
lang = "python")

````

* **Most programming languages supported** Since all our tokenizers are backed by [Tree-Sitter](https://tree-sitter.github.io/tree-sitter/) we support a long list of programming languages. This also includes popular languages such as Python, Java and JavaScript.


## Roadmap
code(dot)tokenize is currently under active development. To enable application for various types of PLP methods, the following features are planned for future versions:

- **Token tagging** Automatically identify certain token types including variable usages, definition and type usages.

- **Syntactic relations** Automatically identify syntactic relations between tokens. This includes read and write relations or structural dependencies.

- **Basic CFG analysis** Automatically identify statement heads which are connected via a control flow.

