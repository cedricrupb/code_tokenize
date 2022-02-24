# Benchmarking

In the following, we benchmark the runtime of **code.tokenize** for parsing Python functions. To obtain a realistic set of Python code for PLP, we employ
the Python portion of the [CodeSearchNet](https://github.com/github/CodeSearchNet) corpus. The corpus includes more than 500K Python functions 
annotated for training.

## Environment 
We benchmark the following implementation in our benchmark:
```python
import code_tokenize as ctok

ctok.tokenize(
    source_code,
    lang = 'python',
    syntax_error = 'raise'
)
```
Therefore, we skip all instances that contain syntax errors. 

For benchmarking, we employ a Macbook Pro M1 with 8GB RAM.

## Results
We start by plotting the mean runtime of the tokenizer in relation
to the size of the Python function (in number of tokens). For determining the size of program, we count the tokens in the pretokenized code. For brevity, we show results for functions below 1024 tokens (since this is the typical size of functions employed in PLP).

<p align="center">
  <img height="150" src="https://github.com/cedricrupb/code_tokenize/raw/main/benchmark/runtime_raise.png" />
</p>

We observe that the time for tokenization scales linearly with the number of tokens in the Python function. Even large function with up to 1024 tokens can be tokenized within 10ms.


## Complete set
Below the uncut version of the diagram. Even for large scale function with
more than 25K tokens, the tokenizer does not take much longer than 100ms.

<p align="center">
  <img height="150" src="https://github.com/cedricrupb/code_tokenize/raw/main/benchmark/runtime_all.png" />
</p>
