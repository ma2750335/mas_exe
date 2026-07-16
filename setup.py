from setuptools import setup, find_packages
with open("README_DS.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name="mas",
    version="0.0.1",
    author="sam",
    packages=find_packages(),
    url="https://github.com/your_org_or_repo",  # optional
    install_requires=[
        "MetaTrader5",
        "numpy",
        "pandas",
        "plotly",
        "quantstats",
        "requests",
        "setuptools",
        "pytz"
    ],
    author="Mas Intelligent Technology Ltd.",
    author_email="service@mindaismart.com",
    description="A Python library for strategy backtesting and trading automation with MetaTrader5.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    python_requires='>=3.8',
)
