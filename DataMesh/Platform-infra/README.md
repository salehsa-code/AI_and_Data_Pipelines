# Wind Data and Analytics platform infrastructure as code framework

## Introduction

The `wind-da-platform-infra` repository contains the code base for
infrastructure automation framework that is used to deploy resources across
`dev`, `test`, `acc` and `prd` environments for Databricks and Azure storage
account resources. The framework code base is written in `hcl` with input
configurations serialized as a set of `yaml` files.

## Repository

The repository structure and content is described below:

| Folder name | Description of contents |
| --- | --- |
| build-scripts | Bootstrap scripts for data products |
| config | Configurations for DTAP and for building data product repositories |
| doc | Documentation for the framework and platform architecture |
| scripts | Init scripts |
| terraform | Terraform framework |
| utils | Utilities required for the framework |

## Build and test

TODO: Describe and show how to build your code and run the tests.

## Contribute

The Terraform framework requires significant skills in the Terraform language.
New features in the framework may be requested to the Data Kong team and bugs
reported in a similar way. The code base is owned and maintained by the Data
Kong team and due to its criticality to the Wind data and analytics platform,
governed strictly. Only the core maintainers are allowed to change the
framework.

Please refer to the [DevOps Guidelines](docs/CONTRIBUTING.md) when contributing
to the framework.

## Usage

The framework is built as a backend engine and in order to use the framework
developers should only ensure that the configuration yaml files for their data
products are properly constructed. No knowledge of the Terraform language is
required to use this framework to build and deploy data products.

## Contact

Please reach out to xxx mailbox for any questions
