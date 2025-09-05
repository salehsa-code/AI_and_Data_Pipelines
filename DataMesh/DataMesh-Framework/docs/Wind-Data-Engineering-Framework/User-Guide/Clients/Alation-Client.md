# Alation Client

## Introduction

The Alation Client is a client that allows you to connect to the Alation Service
and perform operations on it. A common use case is to create and manage
resources in Alation, including creating and managing data sources, uploading
various types of metadata, and managing data lineage.

## How To: Upload Metadata for a Schema

The following examples show how to upload metadata for a Schema in Unity Catalog.

```python
from windef.alation_client import AlationClient

username = "Your Alation username"
password = "Your Alation password"
env = "Your environment (e.g., 'tst' or 'prd')"
client = AlationClient(username, password, env)

# Upload based off of Metadata in Unity Catalog
client.upload_schema_from_unity_catalog("alation_datasource_title", "catalog_name", "schema_name")
# Upload based off of Metadata in the Data products Data Contract
client.upload_data_contract("alation_datasource_title", "/path/to/data_contract/volume/")
```

> :warning: The client will raise a ValueError if the data source title does not start with
> `Wind.VAP2`. This is a safety measure to prevent users from accidentally uploading metadata to
> the wrong data source. It is required, because the technical user in the WDAP environment is
> a system administrator in Alation.

Please refer to the [AlationClient class
Reference](/docs/Reference/alation_client.md) in the provided code for more
examples on how to use the client to interface with the Alation service.

## How To: Upload Data for many Schemas

The following example gives some boilerplate to upload data for many schemas.

```python
# initialize the client as defined above ...

catalog = "Your Unity Catalog"  # e.g. from env variable: os.getenv("CATALOG_DATA_PRODUCTS")

responses = []
schemas_to_upload = [
    {"datasource":"Wind.VAP2.PrimaryProducts", "name":"blade_assets"},
    ...
    {"datasource":"Wind.VAP2.SecondaryProducts", "name":"cable_protection_system"},
    ]

# Option 1: Uplad from data contract
for schema in schemas_to_upload:
    client.upload_data_contract(
        path=f"/Volumes/{catalog}/{schema['name']}/config/data_contract/data_contract.yml",
        datasource_title=schema["datasource"],
    )

# Option 2: Upload from Unity Catalog
for schema in schemas_to_upload:
    client.upload_schema_from_unity_catalog(
        datasource_title=schema["datasource"],
        catalog_name=catalog,
        schema_name=schema["name"],
    )
```
