from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
  name = 'code_tokenize',
  packages = find_packages(exclude=['tests']), 
  version = '0.2.0', 
  license='MIT',     
  description = 'Fast program tokenization and structural analysis in Python',
  long_description = long_description,
  long_description_content_type="text/markdown",
  author = 'Cedric Richter',                   
  author_email = 'cedricr.upb@gmail.com',    
  url = 'https://github.com/cedricrupb/code_tokenize',  
  download_url = 'https://github.com/cedricrupb/code_tokenize/archive/refs/tags/v0.2.0.tar.gz', 
  keywords = ['code', 'tokenization', 'tokenize', 'program', 'language processing'], 
  install_requires=[          
          'tree_sitter',
          'GitPython',
          'requests',
          'code-ast'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',    
    'Intended Audience :: Developers',  
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)