try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "description": "[--]",
    "author": "Vinícius Azambuja",
    "url": "[URL]",
    "download_url": "[URL]",
    "author_email": "vnazambuja@gmail.com",
    "version": "0.1",
    "install_requires": "[--]",
    "packages": "[--]",
    "scripts": "[--]",
    "name": "[NAME]"
}

setup(**config)