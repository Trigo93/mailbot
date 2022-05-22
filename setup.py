from setuptools import setup, find_packages

setup(
    name='mailbot',
    version='0.1.0',
    packages=find_packages(include=['mailbot', 'mailbot.*'])
)
