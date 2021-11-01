from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
  name = 'code_tokenize',
  packages = ['code_tokenize'], 
  version = '0.0.1.post1', 
  license='apache-2.0',     
  description = 'Fast program tokenization and structural analysis in Python',
  long_description = long_description,
  long_description_content_type="text/markdown",
  author = 'Cedric Richter',                   
  author_email = 'cedricr.upb@gmail.com',    
  url = 'https://github.com/cedricrupb/code_tokenize',  
  download_url = 'https://github.com/cedricrupb/code_tokenize/archive/refs/tags/v0.0.1.tar.gz', 
  keywords = ['code', 'tokenization', 'tokenize', 'program', 'language processing'], 
  install_requires=[          
          'tree_sitter',
          'GitPython',
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',    
    'Intended Audience :: Developers',  
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)