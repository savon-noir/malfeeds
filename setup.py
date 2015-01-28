# -*- coding: utf-8 -*-

from distutils.core import setup

with open("README.rst") as rfile:
    long_description = rfile.read()

setup(
    name='maldonne',
    version='0.6.2',
    author='Ronald Bister',
    author_email='mini.pelle@gmail.com',
    packages=['maldonne', 'maldonne.engines', 'maldonne.objects', 'maldonne.feeds'],
    license='Creative Common "Attribution" license (CC-BY) v3',
    description=('Malware feeds librairy'),
    long_description=long_description,
)
