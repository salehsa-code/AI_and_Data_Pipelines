# Table

The `Table` class represents a table in Unity Catalog. It contains necessary
information to create a DDL for the table and provides utility methods to
validate the table definition.

Table objects contain information about the table name, identifier and other
metadata, as well as the tables location on the physical storage and the tables
columns, including partitioning and clustering information.

## How To: Get the schema of the table

You can retrieve the schema of the table using the `schema` property.

```python
schema = table.schema
```

## How To: Add a new column to the table

To add a column to a table, use the `add_column()` method.

```python
new_column = Column(name="new_column", data_type="string")
table.add_column(new_column)
```

## How To: Generate a DDL for the table

To generate the DDL for a table, use the `generate_ddl()` method.

```python
ddl = table.generate_ddl()
```

This method returns a string that represents the DDL of the table.

Additionally, it is possible to add properties and options, when generating the
DDL:

```python
ddl = table.generate_ddl(properties={"prop1": "value1"}, options={"opt1": "value1"})
```

## How To: Set the location of the table

To set the location of a table, use the `set_location()` method.

```python
table = table.set_location("path/to/new_location")
```

This method updates the location of the table and returns the updated table
instance.
