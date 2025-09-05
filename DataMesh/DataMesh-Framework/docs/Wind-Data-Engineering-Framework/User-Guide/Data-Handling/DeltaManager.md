# DeltaManager Module User Guide

The `DeltaManager` module provides a set of functionalities for managing Spark
DataFrames and Delta Tables using PySpark. This guide will walk you through the
process of using the module to perform various operations on Delta tables.

Find a reference of all methods used in this guide
[here](../../../Reference/data_handling.md).

## Initializing the DeltaManager

To begin, we need to initialize the `DeltaManager`. This can be done by creating
a new instance of the class. The `enable_logging_to_azure` parameter allows you
to enable or disable logging to Azure. By default, it is set to `False`.

```python
manager = DeltaManager(enable_logging_to_azure=True)
```

## How To: Getting a DeltaTable

Most of the functionalities in the `DeltaManager` module require a `Table`
object. The `Table` objects for a schema can be created as described in [the Schema module user guide](../Model/Schema.md).

To interact with a Delta table, you first need to get a `DeltaTable` object.
This can be done using the `get_table()` method. This method takes a `Table`
object as a parameter and returns the corresponding `DeltaTable` object.

```python
delta_table = manager.get_table(table)
```

## How To: Creating a Table in Unity Catalog

To create a Delta table in Unity Catalog, you can use the `create_table()`
method. This method takes a `Table` object as a parameter and creates a Delta
table in Unity Catalog.

```python
manager.create_table(table)
```

## How To: Appending Data to a DeltaTable

To append data to a Delta table, you can use the `append_dataframe()` method.
This method takes a `DataFrame` object and a `Table` object as parameters.
Optionally, you can also set the `ignore_empty_df` parameter to `True` if you
want the function to return early without doing anything when the DataFrame is
empty. The table will be refreshed after the data is appended.

```python
manager.append_dataframe(data_frame, table, ignore_empty_df=True)
```

## How To: Merging Data into a DeltaTable

The `merge_dataframe()` method allows you to merge data from a DataFrame into a
Delta table. This method supports update, delete, and insert operations on the
target Delta table based on conditions specified by the user. It also supports
partition pruning to optimize the performance of the merge operation. It will
automatically log the operation metrics (e.g. number of rows updated, deleted,
inserted).

```python
manager.merge_dataframe(data_frame, table)
```

## How To: Deleting a DeltaTable

You can delete a table using the `delete_table()` method. This method requires
you to pass the `table` object and the `table_name` string for security reasons.
If `delete_physical_data` is set to `True`, it will delete not only the metadata
within the Catalog but also the physical data.

```python
manager.delete_table(table, table_name, delete_physical_data=False)
```

Remember to use these functionalities carefully, as operations on Delta tables
are often not reversible. Always ensure that you have backup and recovery
procedures in place.
