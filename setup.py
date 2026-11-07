from setuptools import setup, find_packages

setup(
    name="market-trading-dashboard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=2.2.3",
        "pandas==2.2.3",
        "rich==13.9.4",
        "ta-lib>=0.4.28",
        "yfinance==0.2.51",
    ],
    entry_points={
        "console_scripts": [
            "market-dashboard=market_dashboard.cli:main",
        ],
    },
    author="Prabhash Nandan",
    description="A real-time forex trading dashboard with market analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PrabhashNandan78/market-trading",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
