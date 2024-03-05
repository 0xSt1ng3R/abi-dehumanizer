from setuptools import (
    setup,
    find_packages,
)

setup(
    name="abi_dehumanizer",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="0xSt1ng3R",
    description="A parser for transforming human-readable ABI strings into a format compatible with eth_abi.decode()",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/0xSt1ng3R/abi-dehumanizer",
)
