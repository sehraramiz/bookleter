from setuptools import setup

setup(
    name = 'bookletercli',
    version = '0.1.0',
    packages = ['bookletercli'],
    entry_points = {
        'console_scripts': [
            'bookletercli = bookletercli.__main__:main'
        ]
    })