import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='swb-mlops-azure',
    version='0.0.1',
    install_requires=['requests', 'pyyaml'],
    dependency_links=[],
    author='Erik Peterson',
    author_email='erik.peterson@swedbank.se',
    description='This contains modules utilized in Azure DevOps, Data Factory, & Machine Learning pipelines',
    keywords='mlops, machine learning, ai, databricks',
    license=read('LICENSE.md'),
    url='https://GBI-ODL@dev.azure.com/GBI-ODL/AnalyticsOps/_git/eac_model_template',
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        'Topic :: AnalyticOps :: Utilities',
        'Programming Language :: Python :: 3',
    ]
)