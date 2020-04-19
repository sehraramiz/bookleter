from setuptools import setup
from bookleter.__version__ import __version__

setup(
    name = 'bookleter',
    version = __version__,
    license='MIT',
    description = 'Turns pdfs into a6 sized foldable booklets',
    author = 'Mohsen Barzegar',
    author_email = 'mohsennbarzegar@gmail.com',
    url = 'https://github.com/reinenichts/bookleter',
    download_url = 'https://github.com/reinenichts/bookleter/archive/gui.tar.gz',
    keywords = ['book', 'booklet', 'pdf'],
    packages = ['bookleter'],
    install_requires=[
            'PyPDF2',
            'Pillow',
            'pygubu',
            # 'PyQt5'
        ],
    entry_points = {
        'console_scripts': [
            'bookleter = bookleter.__main__:main'
        ]
    })