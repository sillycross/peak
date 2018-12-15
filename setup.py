from setuptools import setup
import sys

setup(
    name='peak',
    version='0.0.1',
    url='https://github.com/phanrahan/peak',
    license='MIT',
    maintainer='Pat Hanrahan',
    maintainer_email='hanrahan@cs.stanford.edu',
    description='A DSL for Specifying Processors',
    packages=[
        "peak",
    ],
    install_requires=[
        "bit_vector==0.39a0"
    ],
    python_requires='>=3.6'
)