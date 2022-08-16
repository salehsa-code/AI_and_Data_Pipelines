import pathlib
from typing import List

from pkg_resources import parse_requirements
from setuptools import setup, find_packages


def find_dependencies() -> List[str]:
    with pathlib.Path('requirements.txt').open() as requirements_txt:
        return [str(requirement) for requirement in parse_requirements(requirements_txt)]


package = "ot-utils"
version = "0.0.1"
setup(
    name=package,
    version=version,
    packages=find_packages(exclude=["tests", "tests*"]),
    install_requires=find_dependencies()
)
