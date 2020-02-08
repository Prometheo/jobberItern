import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-olaoyejnrscrumy',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='',
    description='A simple Django app to monitor team goals.',
    long_description=README,
    url='',
    author='Popoola Boluwatife',
    author_email='Olaoyejnr@gmail.com',
    classifiers=[
        'Enviroment : : Web Enviroment',
        'Framework : : Django',
        'Framework : : Django : : 3.0',
        'Intended Audience : : Developers',
        'License : : OSI Approved : : BSD License',
        'Operating System : : OS Independent',
        'Programming Language : : Python : : 3.6',
        ]
)
