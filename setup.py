from __future__ import absolute_import
from __future__ import unicode_literals
import os

from setuptools import setup, find_packages

try:
    with open('README.md') as f:
        readme = f.read()
except IOError:
    readme = ''

def _requires_from_file(filename):
    return open(filename).read().splitlines()

# version
here = os.path.dirname(os.path.abspath(__file__))
version = next((line.split('=')[1].strip().replace("'", '')
                for line in open(os.path.join(here,
                                              'sviewgui',
                                              '__init__.py'))
                if line.startswith('__version__ = ')),
               '0.0.dev0')

setup(
    name="sviewgui",
    version=version,
    url='https://github.com/SojiroFukuda/sview-gui',
    author='SojiroFukuda',
    author_email='S.Fukuda-2018@hull.ac.uk',
    maintainer='SojiroFukuda',
    maintainer_email='S.Fukuda-2018@hull.ac.uk',
    description='Package Dependency: Validates package requirements',
    long_description=readme,
    packages=find_packages(),
    install_requires=[
        "sys",
        "PyQt5",
        "numpy",
        "pandas",
        "matplotlib",
        "Pathlib",
        "scipy",
        "cmocean",
        "seaborn",
        "pygments"
    ],
    license="SojiroFukuda",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      sviewstart = sviewgui.sview.command:buildGUI
    """,
)