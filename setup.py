from setuptools import setup
import os

version = "1.0.0.dev0"

long_description = "\n\n".join([open("README.rst").read(), open("CHANGES.rst").read()])

install_requires = ["requests"]

# emulate "--no-deps" on the readthedocs build (there is no way to specify this
# behaviour in the .readthedocs.yml)
if os.environ.get("READTHEDOCS") == "True":
    install_requires = []


tests_require = ["pytest"]

setup(
    name="mopinion-python-api",
    version=version,
    description="API client library for the Mopinion Data API.",
    long_description=long_description,
    # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 1 - Beta",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    keywords=["mopinion"],
    author="Mopinion",
    author_email="",
    url="https://github.com/mopinion/mopinion-python-api.git",
    license="BSD 3-Clause License",
    packages=["mopinion_api"],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    python_requires=">=3.5",
    extras_require={"test": tests_require, "cityhash": ["cityhash"]},
    entry_points={"console_scripts": []},
)
