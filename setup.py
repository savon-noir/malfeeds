# -*- coding: utf-8 -*-

from distutils.core import setup

with open("README.rst") as rfile:
    long_description = rfile.read()

setup(
    name='malfeeds',
    version='0.3',
    author='Ronald Bister',
    author_email='mini.pelle@gmail.com',
    packages=['malfeeds', 'malfeeds.engines', 'malfeeds.objects'],
    license='Creative Common "Attribution" license (CC-BY) v3',
    description=('Malware feeds library'),
    long_description=long_description,
)
