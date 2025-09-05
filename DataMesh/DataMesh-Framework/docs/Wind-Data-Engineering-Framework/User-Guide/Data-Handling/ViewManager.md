# ViewManager Module User Guide

The `ViewManager`s responsibility is to manage views. This currently includes
the creation or update of `SELECT [ALL COLUMNS] for table` views.

## How To: Create Views for a Schema

> Find a description how to create a schema object from the data contract
> [here](../Model/Schema.md#how-to-get-a-table-by-table-name).

```python
# ...
# instantiate the schema object from the data contract
tables = schema.tables

# Create the Views
[view_manager.create_view(t) for t in tables]
```
