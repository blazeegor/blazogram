from setuptools import setup
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / 'README.rst').read_text()


setup(
    name='blazogram',
    version='0.3.1',
    author='EgorBlaze',
    author_email='blazeegor@gmail.com',
    description='BLAZOGRAM - is a library for make Telegram Bots',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/blazeegor/blazogram',
    license='Apache License, Version 2.0, see LICENSE file',
    packages=['blazogram'],
    install_requires=['aiohttp'],
    classifiers=['Intended Audience :: Developers', 'Programming Language :: Python']
)