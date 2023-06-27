import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name="pytest-group-by-class",
    description=(''),
    url='',
    author='',
    author_email='',
    packages=['pytest_group_by_class'],
    version='0.0.1',
    long_description=read('README.md'),
    install_requires=['pytest>=2.5'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Testing',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 ],
    entry_points={
        'pytest11': [
            'test-groups = pytest_group_by_class',
        ]
    },
)
