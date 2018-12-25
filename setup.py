# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-simple-website-meta',
    version='0.0.1',
    author=u'Jon Combe',
    author_email='pypi@joncombe.net',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['metadata_parser',],
    url='https://github.com/joncombe/django-simple-website-meta',
    license='BSD licence, see LICENCE file',
    description='Fetch basic meta data for URLS in Django',
    long_description='Fetch basic meta data for URLS in Django',
    zip_safe=False,
)
