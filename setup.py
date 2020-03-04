from setuptools import setup

setup(
    name = 'bookleter',
    version = '0.1.0',
    packages = ['bookleter'],
    entry_points = {
        'console_scripts': [
            'bookleter = bookleter.__main__:main'
        ]
    })