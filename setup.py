#!/usr/bin/python3
# pzog/setup.py

""" Setuptools project configuration for pzog. """

from os.path import exists
from setuptools import setup

long_desc = None
if exists('README.md'):
    with open('README.md', 'r') as file:
        long_desc = file.read()

setup(name='pzog',
      version='0.6.13',
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      long_description=long_desc,
      packages=['pzog'],
      package_dir={'': 'src'},
      py_modules=[],
      include_package_data=False,
      zip_safe=False,
      scripts=['src/psprog', 'src/pzogd', 'src/ring_data_gen'],
      ext_modules=[],
      description='organize ring of 5-6 machines sharing data over full mesh',
      url='https://jddixon.github.io/pzog',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python 2',
          'Programming Language :: Python 2.7',
          'Programming Language :: Python 3',
          'Programming Language :: Python 3.5',
          'Programming Language :: Python 3.6',
          'Programming Language :: Python 3.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],)
