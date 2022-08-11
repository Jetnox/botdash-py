from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name = 'botdash.py',
    version = '2.1.5',
    url = 'https://github.com/TBTech205/botdash-py',
    license = 'MIT',
    author = 'TBTECH205',
    description = 'API wrapper for botdash.pro',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    keywords = [
        'botdash',
        'discord',
        'bot'
    ],
    install_requires = [
        'setuptools',
        'requests',
        'six',
        'ujson'
    ],
    setup_requires = [
        'wheel'
    ],
    packages = find_packages()
)
