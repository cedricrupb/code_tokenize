from distutils.core import setup

setup(
  name = 'code_tokenize',
  packages = ['code_tokenize'], 
  version = '0.0.1', 
  license='apache-2.0',     
  description = 'TYPE YOUR DESCRIPTION HERE',
  author = 'Cedric Richter',                   
  author_email = 'cedricr.upb@gmail.com',    
  url = 'https://github.com/cedricrupb/code_tokenize',  
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',  # TODO
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
    'License :: OSI Approved :: Apache License 2.0',
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)