"""
Setup script for AI Agent package
"""
from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "AI Agent - Intelligent macOS automation through natural language"

# Read requirements
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return ["google-generativeai>=0.3.0"]

setup(
    name="ai-agent",
    version="1.0.0",
    author="AI Agent Development Team",
    author_email="contact@example.com",
    description="Intelligent macOS automation through natural language",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/example/ai-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-agent=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="macos automation applescript shell ai gemini natural-language",
    project_urls={
        "Bug Reports": "https://github.com/example/ai-agent/issues",
        "Source": "https://github.com/example/ai-agent",
        "Documentation": "https://ai-agent.readthedocs.io",
    },
)