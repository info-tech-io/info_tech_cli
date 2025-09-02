"""
InfoTech CLI - Command-line interface for InfoTech.io educational platform
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="info_tech_cli",
    version="0.1.0",
    author="A1eksMa",
    author_email="a1ex_ma@mail.ru",
    description="Command-line interface for InfoTech.io educational platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/info-tech-io/info_tech_cli",
    project_urls={
        "Bug Tracker": "https://github.com/info-tech-io/info_tech_cli/issues",
        "Documentation": "https://github.com/info-tech-io/info_tech_cli#readme",
        "Source Code": "https://github.com/info-tech-io/info_tech_cli",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Education",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "info_tech_cli=info_tech_cli.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "info_tech_cli": [
            "templates/*",
            "templates/module-basic/*",
        ],
    },
    keywords="education, cli, hugo, learning, module-generator, infotecha",
    zip_safe=False,
)