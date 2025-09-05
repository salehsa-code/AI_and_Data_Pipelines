# Unity Catalog Adapter

## Introduction

The Unity Catalog Adapter serves as an Adapter between WinDEF models and Unity Catalog.

## How To: Derive a WinDEF Schema from Unity Catalog Metadata

The following example shows how to get a complete WinDEF-`Schema` derived from a UC-Catalog.

```python
from windef.models import UnityCatalogAdapter

adapter = UnityCatalogAdapter()
schema = adapter.get_schema_by_name(catalog_name, schema_name)
```

The schema can then be used to access the list of Tables and their Columns for further usage.

```python
# get a list of all Table objects in the Schema
tables = schema.tables
# or access a specific Table
table = schema.get_table_by_name("my_table")
for column in table.columns:
    # do something
```

Please refer to the [UnityCatalogAdapter class
reference](/docs/Reference/models.md#adapterunity_catalog_adapter) in the
provided code for more examples on how to use it.
