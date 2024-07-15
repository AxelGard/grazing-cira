from setuptools import setup

with open("./README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="grazing",
    version="0.1.0",
    description="Cira set in production",
    url="https://github.com/AxelGard/grazing-cira",
    author="Axel Gard",
    author_email="axel.gard@tutanota.com",
    license="MIT",
    packages=[
        "grazing", 
        "grazing.features",
        "grazing.strategies",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "cira",
        "matplotlib",
        "scikit-learn",
        "pandas",
        "numpy",
        "pyyaml",
    ],
    extras_requires={"dev": ["pytest"]},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)
