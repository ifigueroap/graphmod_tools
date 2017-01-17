from setuptools import setup

setup(  name = 'graphmod_tools'
      , version = '0.1'
      , description = 'Simple library for managing static Haskell dependencies created with GraphMod'
      , url = 'http://github.com/ifigueroap/graphmod_tools'
      , author = 'Ismael Figueroa'
      , author_email = 'ifigueroap@gmail.com'
      , license = 'MIT'
      , packages = ['graphmod_tools']
      , zip_safe = False
      , install_requires = [
        'pydotplus'
      ]
      , scripts = ['bin/graph-deps'] )
