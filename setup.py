"""Setup script for the CodeBots SDK."""
from setuptools import setup, find_packages

setup(
    name="codebots-arena",
    version="0.1.0",
    description="AI vs AI Code Battle Arena — write your bot",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Mohammed Ghabban",
    author_email="734402368n@gmail.com",
    url="https://github.com/Mhmda1998/CodeBots-Arena",
    license="MIT",
    packages=find_packages(where="sdk"),
    package_dir={"": "sdk"},
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment",
        "Topic :: Education",
    ],
)
