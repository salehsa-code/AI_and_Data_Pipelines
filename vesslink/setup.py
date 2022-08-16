from setuptools import setup, find_packages

with open('requirements.txt') as requirements:
    dependencies = requirements.read().strip().split("\n")

package = "vesslink-api-cli"
version = "1.0.0"
setup(
    name=package,
    version=version,
    packages=find_packages(exclude=["tests", "tests*"]),
    install_requires=dependencies
)
