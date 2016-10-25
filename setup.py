#!/usr/bin/python3

# ~/dev/py/pzog/setup.py

import re
from distutils.core import setup
__version__ = re.search(r"__version__\s*=\s*'(.*)'",
                        open('pzog/__init__.py').read()).group(1)

# see http://docs.python.org/distutils/setupscript.html

setup(name='pzog',
      version=__version__,
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      #
      # wherever we have a .py file that will be imported, we
      # list it here, without the extension but SQuoted
      py_modules=[],
      #
      # a package has a subdir and an __init__.py
      packages=['pzog', ],
      #
      # following could be in scripts/ subdir; SQuote
      scripts=['psprog', 'pzogd', 'ring_data_gen'],
      description='software organizing a ring of 5-6 machines sharing data over a full mesh',
      url='https://jddixon.github.io/pzog',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python 3',
      ],)
