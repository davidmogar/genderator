#!/user/bin/env python

import re, uuid

from pip.req import parse_requirements
from setuptools import setup, find_packages


version = re.search(
    '^__version__\s*=\s*\'(.*)\'',
    open('genderator/__init__.py').read(),
    re.M).group(1)

with open("README.rst", "rb") as f:
    long_description = f.read().decode("utf-8")

install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())
reqs = [str(req.req) for req in install_reqs]

setup(name='genderator',
      version=version,
      description='Python library to guess gender given a spanish full name',
      long_description=long_description,
      author='David Moreno-Garcia',
      author_email='david.mogar@gmail.com',
      license='MIT',
      url='https://github.com/davidmogar/genderator',
      download_url='https://github.com/davidmogar/genderator/tarball/' + version,
      keywords=['gender', 'guess', 'spanish', 'name'],
      packages=find_packages(exclude=['tests']),
      install_requires=reqs,
      include_package_data=True,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Topic :: Software Development :: Libraries',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
      ]
      )
