#!/usr/bin/env python
from setuptools import find_packages, setup


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
]

# extras_requirements = {
# }

setup_requirements = [
]

test_requirements = [
]

# TODO: extract from '__version__' in 'fd_gcp/__init__.py'.
packages_version = '0.1.0'

# note: the "typing information" of this project's packages is not made available to its users
#   automatically; it needs to be packaged and distributed. The way to do so is fairly new and
#   it is specified in PEP 561 - "Distributing and Packaging Type Information".
#   See:
#   - https://www.python.org/dev/peps/pep-0561/#packaging-type-information
#   - https://github.com/python/typing/issues/84
#   - https://github.com/python/mypy/issues/3930
_package_data = {
    'fd_gcp': [
        # Indicates that the "typing information" of the package should be distributed.
        'py.typed',
    ],
}

setup(
    author="Fyndata",
    author_email='no-reply@fyndata.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description="Fyndata's Python library of Google Cloud Platform (GCP) utils.",
    # extras_require=extras_requirements,
    install_requires=requirements,
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
    version=packages_version,
    zip_safe=False,
)
