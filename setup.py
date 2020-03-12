from os import path
from setuptools import setup, find_namespace_packages

__version__ = "0.0.1"

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

with open(path.join(here, "requirements-dev.txt"), encoding="utf-8") as f:
    dev_reqs = f.read().split("\n")

setup(
    name="covid-health-ita",
    version=__version__,
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Giacomo Barone, Buildnn",
    url="https://www.buildnn.com",
    license="Copyright © 2020 Giacomo Barone / Buildnn. MIT.",
    classifiers=[],
    package_dir={"": "src"},
    packages=find_namespace_packages(
        where="src", include=["*"], exclude=["*.egg-info"]
    ),
    include_package_data=True,
    keywords="",
    install_requires=all_reqs,
    extras_require={"dev": dev_reqs},
    # dependency_links=dependency_links,
    author_email="giacomo.barone@buildnn.com",
    entry_points="""
        [console_scripts]
        covid-data=covid_health_it.cli:main
    """,
)
