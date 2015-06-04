try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name="imgutils",
    version='0.1.0',
    author="Dan Bradham",
    author_email="danielbradham@gmail.com",
    url="https://github.com/danbradham/imgutils",
    py_modules=["imgutils"],
    description="Useful image utilities",
    long_description=long_description,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ]
      )
