# (P)tokenizers

A library for fast AST backed **p**rogram **tokenization**.

## AST backed tokenization
Programminng Language Processing (PLP) brings the capabilities of modern NLP systems to the world of programming languages. 
To achieve high performance PLP systems,existing methods often take advantage of the fully defined nature of programminng languages. Especially the syntactical structure can be exploited.

AST backed tokenization provide easy access to the syntactic structure of a program. The tokenizer converts a program into a sequence of program tokens ready for further end-to-end processing.
By relating each token to an AST node, it is possible to extend the program representation easily with further syntactic information.

## Library highlights
Whether you are on the search for a fast multilingual program tokenizer or want to start your next PLP project, here are some reason why you should build upon ptokenizers:

* **Easy to use** All it takes to tokenize your code is to run a single line:
````
import ptokenizers as ptok

ptok.tokenize(
    '''
        def my_func():
            print("Hello World")
    ''',
lang = "python")

````

* **Most programming languages supported** Since all our tokenizers are backed by [Tree-Sitter](https://tree-sitter.github.io/tree-sitter/) we support a long list of programming languages. This also includes popular languages such as Python, Java and JavaScript.
