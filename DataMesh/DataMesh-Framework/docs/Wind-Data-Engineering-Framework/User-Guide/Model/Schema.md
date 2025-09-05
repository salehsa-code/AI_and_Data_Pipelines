# Schema

The `Schema` class represents a schema belonging to a data product or data
source. The schema contains the name of the data catalog it is in, as well as a
list of datasets that are part of that schema.

Generally, it is not expected to create the schema class manually, but rather
create it from the data contract using the `read_instance_from_file` classmethod.

## How To: Get a table by table name

```python
from pathlib import Path

from windef.models import Schema

schema, errors = Schema.read_instance_from_file(Path('path/to/schema.yml'))
# errors contains a list of errors that occurred during the creation of the schema
table = schema.get_table_by_name('table_name')

# or you can create a new table object directly
table, errors = Table.read_instance_from_file(Path('path/to/table.yml'))
# errors contains a list of errors that occurred during the creation of the table
```

If the table is not part of the schema, the method raises a `ValueError`. During
creation of the instances, the metadata is validated.

## How To: Add a new table to the schema

> :warning: Generally, all tables of a schema should be part of the data
> contract. However, for development purposes it might be useful to manually add
> new tables to an existing schema object. **Be aware, that there is currently
> no check for duplicate tables using this method.**

To add a table to a schema, use the `add_table()` method.

```python
new_table = Table(name="new_table", format="delta")
schema.add_table(new_table)
```

## How To: Generate all Tables in a Data Contract

The Schema model provides capabilities to generate `Table` and
`Schema` objects. These in turn can generate a valid SQL DDL Statement for
themselves. To execute these statements, you can use the Delta Manager module.

```python
from windef.models import Schema
from windef.data_handling import DeltaManager

schema, errors = Schema.read_instance_from_file(Path('path/to/schema.yml'))
# raise an error, if errors is not an empty list (if required)

delta_manager = DeltaManager()

for table in schema.tables:
    delta_manager.create_table(table)
```

The `create_table` method will use the Tables `generate_ddl` method to create a
valid DDL and execute it using the delta_managers Spark session. It also
prepends the correct `USE CATALOG` and `USE SCHEMA` statements to the DDL.
