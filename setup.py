from setuptools import setup

setup(
    name = 'bookleter',
    version = '0.1.0',
    license='MIT',
    description = 'turns pdfs into a6 sized foldable booklets',
    author = 'Mohsen Barzegar',
    author_email = 'mohsennbarzegar@gmail.com',
    url = 'https://github.com/reinenichts/bookleter',
    download_url = 'https://github.com/reinenichts/bookleter/archive/first.tar.gz',
    keywords = ['book', 'booklet', 'pdf'],
    packages = ['bookleter'],
    install_requires=[
            'PyPDF2',
            'Pillow',
            'pdfCropMargins'
        ],
    entry_points = {
        'console_scripts': [
            'bookleter = bookleter.__main__:main'
        ]
    })