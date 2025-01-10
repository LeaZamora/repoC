# setup.py
from setuptools import setup, find_packages


setup(
    name="doxLogParser",
    version="0.1.0",
    packages=find_packages(),
    install_requires=['pytest'],  # List of external dependencies, if any
    test_suite="tests",
    include_package_data=True,
    description="A simple example Python package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Lea Zamora",
    author_email="",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)