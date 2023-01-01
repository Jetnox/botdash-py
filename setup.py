from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name = 'botdash.py-dev',
    version = '1.0.1',
    url = 'https://github.com/jetnox/botdash-py',
    download_url = 'https://github.com/jetnox/botdash-py/tarball/master',
    license = 'MIT',
    author = 'Jetnox',
    author_email = 'support@jetnox.org',
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
        'ujson',
        'python-socketio'
    ],
    setup_requires = [
        'wheel'
    ],
    packages = find_packages()
)
