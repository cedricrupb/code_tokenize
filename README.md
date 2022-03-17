<p align="center">
  <img height="150" src="https://github.com/cedricrupb/ptokenizers/raw/main/resources/code_tokenize.svg" />
</p>

------------------------------------------------
> Fast tokenization and structural analysis of
any programming language in Python

Programming Language Processing (PLP) brings the capabilities of modern NLP systems to the world of programming languages. 
To achieve high performance PLP systems, existing methods often take advantage of the fully defined nature of programming languages. Especially the syntactical structure can be exploited to gain knowledge about programs.

**code.tokenize** provides easy access to the syntactic structure of a program. The tokenizer converts a program into a sequence of program tokens ready for further end-to-end processing.
By relating each token to an AST node, it is possible to extend the program representation easily with further syntactic information.

## Installation
The package is tested under Python 3. It can be installed via:
```
pip install code-tokenize
```

## Usage
code.tokenize can tokenize nearly any program code in a few lines of code:
```python
import code_tokenize as ctok

# Python
ctok.tokenize(
    '''
        def my_func():
            print("Hello World")
    ''',
lang = "python")

# Output: [def, my_func, (, ), :, #NEWLINE#, ...]

# Java
ctok.tokenize(
    '''
        public static void main(String[] args){
          System.out.println("Hello World");
        }
    ''',
lang = "java", 
syntax_error = "ignore")

# Output: [public, static, void, main, (, String, [, ], args), {, System, ...]

# JavaScript
ctok.tokenize(
    '''
        alert("Hello World");
    ''',
lang = "javascript", 
syntax_error = "ignore")

# Output: [alert, (, "Hello World", ), ;]


```

## Supported languages
code.tokenize employs [tree-sitter](https://tree-sitter.github.io/tree-sitter/) as a backend. Therefore, in principal, any language supported by tree-sitter is also
supported by a tokenizer in code.tokenize.

For some languages, this library supports additional
features that are not directly supported by tree-sitter.
Therefore, we distinguish between three language classes
and support the following language identifier:

- `native`: python
- `advanced`: java
- `basic`: javascript, go, ruby, cpp, c, swift, rust, ...

Languages in the `native` class support all features 
of this library and are extensively tested. `advanced` languages are tested but do not support the full feature set. Languages of the `basic` class are not tested and
only support the feature set of the backend. They can still be used for tokenization and AST parsing.

## Release history
* 0.1.0
    * The first proper release
    * CHANGE: Language specific tokenizer configuration
    * CHANGE: Basic analyses of the program structure and token role
    * CHANGE: Documentation
* 0.0.1
    * Work in progress

## Project Info
The goal of this project is to provide developer in the
programming language processing community with easy
access to program tokenization and AST parsing. This is currently developed as a helper library for internal research projects. Therefore, it will only be updated
as needed.

Feel free to open an issue if anything unexpected
happens. 

Distributed under the MIT license. See ``LICENSE`` for more information.

This project was developed as part of our research related to:
```bibtex
@inproceedings{richter2022tssb,
  title={TSSB-3M: Mining single statement bugs at massive scale},
  author={Cedric Richter, Heike Wehrheim},
  booktitle={MSR},
  year={2022}
}
```

We thank the developer of [tree-sitter](https://tree-sitter.github.io/tree-sitter/) library. Without tree-sitter this project would not be possible. 
