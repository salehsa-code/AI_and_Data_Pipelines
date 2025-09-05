# Add wheel to JFrog artifactory as library for PIP

This file will explain how we can deploy a python wheel file to jfrog in order to be able to install in with pip in Databricks.

## Why we need this?

In WDAP we can't download libraries directly when it is not available through pip.
For that the jfrog artifactory has been created.
In this artifectory the code will be scanned for vulnarabilities using Xray. This guarantees us from using unsecure code.

## Download whl file

First step is to download your whl file yourself. This can be done on your laptop.

For example: https://spacy.io/models/en/#en_core_web_sm This wheel contains models for anonimization and isn't available throught the standard pip repository.

## How to add the wheel to JFrog

Our jfrog artifactory repo can be found here: https://registry-se.corp.vattenfall.com/ui/repos/tree/General/local-pyp-wind-data

You need to login. The login username and credetials can be taken from keyvault: https://portal.azure.com/#@Vattenfall.onmicrosoft.com/resource/subscriptions/45009243-9df4-49ec-8872-8beef91f7db9/resourceGroups/vap2-devtst-infra-security-we-rg/providers/Microsoft.KeyVault/vaults/vap2-dev-winddata-cmn-kv/secrets
The secret for the s1winddata user can be found here.

In jfrog you need to deploy the wheel as following:
- Go to the Artifacts
- Select the reposity: local-pyp-wind-data
- Press Deploy button on top
- Drop file

## How to install this library?

In Databricks the connection to JFrog has already been established (firewall opening, etc).

Installation of the library is exactly the same as all other libraries:

```
pip install <<Library from jfrog>>
```
Use here the name without the .whl extension.

Happy coding!

