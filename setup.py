#  -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='ictrlquotes',
    version='0.2',
    license='GPL',
    author='Andreas Schulz',
    author_email='andi.schulz@me.com',
    description='Quotes form (in)famous people at ictrl.',
    packages=find_packages(),
    package_data={'ictrlquotes': ['widgets/ui/mainwindow.ui',
                                  'widgets/ui/addauthordialog.ui',
                                  'res/reload.png']},
    scripts=['bin/ictrlquotes'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Not special register people',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Fun',
    ],
)
