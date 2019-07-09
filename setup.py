#!/usr/bin/env python
import os
import re
from typing import Sequence

from setuptools import find_packages, setup


def get_version(*file_paths: Sequence[str]) -> str:
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version('fd_gcp', '__init__.py')


with open('README.md') as readme_file:
    readme = readme_file.read()

# TODO: add reasonable upper-bound per package.
requirements = [
    'cryptography>=2.7',
    'google-api-python-client>=1.7.9',
    'google-auth>=1.6.3',
    'requests>=2.22.0',
]

# extras_requirements = {
# }

setup_requirements = [
]

test_requirements = [
    # note: include here only packages **imported** in test code (e.g. 'requests-mock'), NOT those
    #   like 'coverage' or 'tox'.
]

# note: the "typing information" of this project's packages is not made available to its users
#   automatically; it needs to be packaged and distributed. The way to do so is fairly new and
#   it is specified in PEP 561 - "Distributing and Packaging Type Information".
#   See:
#   - https://www.python.org/dev/peps/pep-0561/#packaging-type-information
#   - https://github.com/python/typing/issues/84
#   - https://github.com/python/mypy/issues/3930
# warning: remember to replicate this in the manifest file for source distribution ('MANIFEST.in').
_package_data = {
    'fd_gcp': [
        # Indicates that the "typing information" of the package should be distributed.
        'py.typed',
    ],
}

setup(
    author='Fyndata (Fynpal SpA)',
    author_email='no-reply@fyndata.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description="Fyndata's Python library of Google Cloud Platform (GCP) utils.",
    # extras_require=extras_requirements,
    install_requires=requirements,
    license="MIT",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    name='fyndata-gcp-utils',
    package_data=_package_data,
    packages=find_packages(exclude=['docs', 'tests*']),
    python_requires='>=3.7, <3.8',
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/fyndata/gcp-utils-python',
    version=version,
    zip_safe=False,
)
