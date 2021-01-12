from setuptools import setup
import os

version = "1.0.0"

long_description = "\n\n".join([open("README.md").read(), open("CHANGES.md").read()])

install_requires = [
    "requests>=2.0.0",
    "pydantic>=1.7.0"
]

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
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["mopinion"],
    author="Mopinion",
    author_email="",
    url="https://github.com/mopinion/mopinion-python-api.git",
    license="MIT License",
    packages=["mopinion_api"],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    python_requires=">=3.6",
    extras_require={"test": tests_require, "cityhash": ["cityhash"]},
    entry_points={"console_scripts": []},
)
