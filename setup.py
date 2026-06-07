"""
setup.py — installation script for TDE (The Data Encoder/Decoder).

Install globally with:
    pip install .

After installation the `tde` command is available system-wide.
"""

from setuptools import setup, find_packages

setup(
    name="tde",
    version="1.0.0",
    description="TDE — The Data Encoder/Decoder. A fast, dependency-free Base64 CLI tool.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="you@example.com",
    url="https://github.com/yourusername/tde-tool",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],            # Zero external dependencies — by design
    entry_points={
        "console_scripts": [
            "tde=tde.cli:main",     # `tde` command → tde/cli.py → main()
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Security :: Cryptography",
        "Topic :: Utilities",
    ],
)
