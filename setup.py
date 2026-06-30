from setuptools import setup, find_packages

setup(
    name="tde",
    version="1.1.0",
    description="TDE — Tanishq's Decoder & Encoder. A fast, dependency-free multi-format encoding CLI tool (Base64, Hex, Base32, Base85).",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Tanishq Zope",
    author_email="tanishqzope5@gmail.com",
    url="https://github.com/tanishqzope/TDE-Tool",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],            
    entry_points={
        "console_scripts": [
            "tde=tde.cli:main",   
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Security :: Cryptography",
        "Topic :: Text Processing :: General",
        "Topic :: Utilities",
    ],
)
