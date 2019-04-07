import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-3xbit",
    version="0.1",
    author="marciks",
    author_email="marcinhocfa@gmail.com",
    description="A python 3xbit wrapper",
    url="https://github.com/marciks/python-3xbit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
