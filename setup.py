#! /usr/bin/env python3

from setuptools import setup

setup(
    name='temp_sentry',
    author='Justin Hildreth',
    version='0.1.0',
    license='MIT',
    packages=[
      'temp_sentry'
    ],
    entry_points={
        'console_scripts': [
            'temp_sentry = temp_sentry.__main__:main',
        ],
    },
    install_requires=[
        'w1thermsensor',
        'twilio'
    ],
)