from setuptools import setup

import os


version = "0.0.6"

long_description = "\n\n".join([open("README.rst").read(), open("CHANGES.rst").read()])

install_requires = [
    "requests",
    "dataclasses; python_version < '3.7.0'",
]

# emulate "--no-deps" on the readthedocs build (there is no way to specify this
# behaviour in the .readthedocs.yml)
if os.environ.get("READTHEDOCS") == "True":
    install_requires = []


tests_require = [
    "requests",
    "pytest",
    "mock",
    "dataclasses; python_version < '3.7.0'",
]

setup(
    name="mopinion",
    version=version,
    description="A client library for the Mopinion Data API",
    long_description=long_description,
    # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["mopinion"],
    author="Mopinion",
    author_email="",
    url="https://github.com/mopinion/mopinion-python-api",
    license="MIT License",
    packages=["mopinion"],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    python_requires=">=3.6",
    extras_require={"test": tests_require},
    entry_points={"console_scripts": []},
)
