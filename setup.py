from os import path
from setuptools import setup, find_packages

with open(path.join(path.abspath(path.dirname(__file__)), 'Readme.md'), encoding='utf-8') as f:
    long_description = f.read()



setup(name='tystream',
      version='1.5.4',
      author='Mantouisyummy',
      author_email='opcantel@gmail.com',
      description='A Python library for Twitch & Youtube Stream Notification.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/Mantouisyummy/TYStream',
      project_urls={
          'Issue Tracker': 'https://github.com/Mantouisyummy/TYStream'
      },
      install_requires=[
          "requests>=2.25.0",
          "colorlog>=6.8.2",
          "aiohttp>=3.8.6"
      ],
      packages=find_packages(),
      keywords=['Twitch', 'Youtube', 'stream', 'stream Notification', 'Notification'],
      license='GNU',
      classifiers=[
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
          'Natural Language :: English'
      ],
      python_requires='>=3.10'
)
