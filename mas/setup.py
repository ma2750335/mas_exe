from setuptools import setup, find_packages

setup(
    name="mas_trading_platform",
    version="0.1.0",
    description="A modular algorithmic trading library for MT5 with backtesting and GUI support.",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/your_org_or_repo",  # optional
    packages=find_packages(exclude=["tests", "examples"]),
    include_package_data=True,
    install_requires=[
        "MetaTrader5>=5.0",       # 需使用 pip install MetaTrader5
        "pandas>=1.3",
        "numpy>=1.21",
        "plotly>=5.0",
        "quantstats>=0.0.62",
        "sqlalchemy>=1.4",
        "PySide6>=6.4"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    entry_points={
        "console_scripts": [
            # 若有 CLI，可填寫如:
            # "mas-cli = mas.cli:main"
        ]
    }
)
