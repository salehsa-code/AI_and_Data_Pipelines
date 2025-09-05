# Table of Contents

* [delta\_manager](#delta_manager)
* [schema\_handler](#schema_handler)
* [view\_manager](#view_manager)
* [delta\_operations](#delta_operations)
* [data\_replication](#data_replication)
* [data\_replication.data\_replication\_config](#data_replication.data_replication_config)
* [data\_replication.data\_replication\_service](#data_replication.data_replication_service)
* [writer](#writer)
* [writer.writer](#writer.writer)
* [writer.table\_writer](#writer.table_writer)
* [writer.kafka\_writer](#writer.kafka_writer)
* [writer.file\_writer](#writer.file_writer)
* [reader](#reader)
* [reader.api\_reader](#reader.api_reader)
* [reader.file\_reader](#reader.file_reader)
* [reader.volume\_reader](#reader.volume_reader)
* [reader.reader](#reader.reader)
* [reader.kafka\_reader](#reader.kafka_reader)
* [reader.table\_reader](#reader.table_reader)
* [reader.excel\_reader](#reader.excel_reader)
* [delta\_loader](#delta_loader)
* [delta\_loader.delta\_loader\_metadata\_table](#delta_loader.delta_loader_metadata_table)
* [delta\_loader.delta\_loader\_factory](#delta_loader.delta_loader_factory)
* [delta\_loader.delta\_loader](#delta_loader.delta_loader)
* [delta\_loader.strategies.delta\_cdf\_loader](#delta_loader.strategies.delta_cdf_loader)
* [delta\_loader.strategies](#delta_loader.strategies)
* [delta\_loader.strategies.delta\_timestamp\_loader](#delta_loader.strategies.delta_timestamp_loader)

<h1 id="delta_manager">delta_manager</h1>

<h2 id="delta_manager.MergeConfig">MergeConfig</h2>

```python
class MergeConfig(BaseModel)
```

A class to hold the configuration for the merge functions.

**Arguments**:

- `table` _Table_ - A Table object representing the Delta table.
- `data_frame` _DataFrame_ - The DataFrame to be merged into the Delta table.
- `key_columns` _list[str], optional_ - List of column names that form the key for the merge
  operation. Defaults to the primary key of the table.
- `when_matched_update` _bool, optional_ - Flag to specify whether to perform an update
  operation when matching records are found in the target Delta table. Defaults to True.
- `when_matched_deleted` _bool, optional_ - Flag to specify whether to perform a delete
  operation when matching records are found in the target Delta table. Defaults to False.
- `when_not_matched_insert` _bool, optional_ - Flag to specify whether to perform an insert
  operation when matching records are not found in the target Delta table. Defaults to
  True.
- `cols_to_update` _dict[str, str], list[str], optional_ - List of column
  names to be updated in the target Delta table. If a dict is given,
  this is taken as final mapping for col updates. Defaults to columns of df.
- `cols_to_insert` _list[str], optional_ - List of column names to be
  inserted into the target Delta table. Defaults to columns of df.
- `cols_to_exclude` _list[str], optional_ - List of column names to be excluded from the merge
  operation. Defaults to None.
- `use_partition_pruning` _bool, optional_ - Flag to specify whether to use partition pruning to
  optimize the performance of the merge operation. Defaults to True.
- `ignore_empty_df` _bool, optional_ - A flag indicating whether to ignore an empty source
  dataframe. Defaults to False.

<h4 id="delta_manager.MergeConfig.data_frame">data_frame</h4>

actually a DataFrame, but we can't import the remote version

<h4 id="delta_manager.MergeConfig.cols_to_merge">cols_to_merge</h4>

set through model_validator

<h4 id="delta_manager.MergeConfig.final_cols_to_update">final_cols_to_update</h4>

set through model_validator

<h4 id="delta_manager.MergeConfig.final_cols_to_insert">final_cols_to_insert</h4>

set through model_validator

<h2 id="delta_manager.EmptyDataframeException">EmptyDataframeException</h2>

```python
class EmptyDataframeException(Exception)
```

When a dataframe is empty when it should not be.

<h2 id="delta_manager.DeltaManager">DeltaManager</h2>

```python
class DeltaManager()
```

A class to manage Delta tables in a Spark Session.

<h4 id="delta_manager.DeltaManager.get_table">get_table</h4>

```python
def get_table(table: Table) -> DeltaTable
```

Get the DeltaTable object from the Table objects location.

**Arguments**:

- `table` _Table_ - A Table object representing the Delta table.
  

**Returns**:

- `DeltaTable` - The DeltaTable object corresponding to the given Table
  object.

<h4 id="delta_manager.DeltaManager.table_exists">table_exists</h4>

```python
def table_exists(table: Table) -> bool
```

Checks if a table exists in the catalog.

**Arguments**:

- `table` _Table_ - A Table object representing the Delta table.
  

**Returns**:

- `bool` - True if the table exists, else False.

<h4 id="delta_manager.DeltaManager.overwrite_dataframe">overwrite_dataframe</h4>

```python
@LoggingService.table_log_decorator(operation="overwrite")
def overwrite_dataframe(table: Table,
                        data_frame: DataFrame,
                        ignore_empty_df: bool = False,
                        options: dict[str, str] | None = None)
```

Appends the provided DataFrame to a Delta table.

**Arguments**:

- `table` _Table_ - A Table object representing the Delta table.
- `data_frame` _DataFrame_ - The DataFrame to overwrite the table with.
- `ignore_empty_df` _bool_ - If True, the function returns early without
  doing anything if the DataFrame is empty. Defaults to False.
- `options` - Additional keyword arguments that will be passed to the 'write' method of the
  FileDataFrameWriter instance. These can be any parameters accepted by the 'write'
  method, which could include options for configuring the write operation, such as
  'checkpointLocation' for specifying the path where checkpoints will be stored, or
  'path' for specifying the path where the output data will be written.
  

**Returns**:

  None.

<h4 id="delta_manager.DeltaManager.append_dataframe">append_dataframe</h4>

```python
@LoggingService.table_log_decorator(operation="append")
def append_dataframe(table: Table,
                     data_frame: DataFrame,
                     ignore_empty_df: bool = False,
                     options: dict[str, str] | None = None)
```

Appends the provided DataFrame to a Delta table.

**Arguments**:

- `table` _Table_ - A Table object representing the Delta table.
- `data_frame` _DataFrame_ - The DataFrame to append to the table.
- `ignore_empty_df` _bool_ - If True, the function returns early without
  doing anything if the DataFrame is empty. Defaults to False.
- `options` - Additional keyword arguments that will be passed to the 'write' method of the
  FileDataFrameWriter instance. These can be any parameters accepted by the 'write'
  method, which could include options for configuring the write operation, such as
  'checkpointLocation' for specifying the path where checkpoints will be stored, or
  'path' for specifying the path where the output data will be written.
  

**Returns**:

  None.

<h4 id="delta_manager.DeltaManager.append_dataframe_stream">append_dataframe_stream</h4>

```python
@LoggingService.table_log_decorator(operation="stream_append")
def append_dataframe_stream(table: Table,
                            data_frame: DataFrame,
                            ignore_empty_df: bool = False,
                            checkpoint_location: str | None = None,
                            trigger: str = "once",
                            trigger_specification: str | None = None,
                            options: dict[str, str] | None = None)
```

Appends the provided DataFrame to a Delta table.

**Arguments**:

- `table` _Table_ - A Table object representing the Delta table.
- `data_frame` _DataFrame_ - The DataFrame to append to the table.
- `ignore_empty_df` _bool_ - If True, the function returns early without
  doing anything if the DataFrame is empty. Defaults to False.
- `checkpoint_location` _str_ - Location of checkpoint. If None, defaults
  to the location of the table being written, with '_checkpoint_'
  added before name. Default None.
- `trigger` _str_ - Trigger. Default 'once', recommended to not change
  unless you know what you're doing.
- `trigger_specification` _str_ - Specification for chosen trigger (e.g.
  "5 seconds" for processingTime). Only useful for processingTime
  and continuous.
- `options` - Additional keyword arguments that will be passed to the
  'write' method of the FileDataFrameWriter instance. These can be
  any parameters accepted by the 'write' method, which could
  include options for configuring the write operation.
  

**Returns**:

  None.

<h4 id="delta_manager.DeltaManager.refresh_table">refresh_table</h4>

```python
@LoggingService.table_log_decorator(operation="refresh")
def refresh_table(table: Table)
```

Refreshes the metadata of a Delta table.

**Arguments**:

- `table` _Table_ - A Table object representing the Delta table.
  

**Returns**:

  None.

<h4 id="delta_manager.DeltaManager.merge_dataframe">merge_dataframe</h4>

```python
@LoggingService.table_log_decorator(operation="merge")
def merge_dataframe(**kwargs)
```

Merges the data in a spark DataFrame into a Delta table.

This function performs a merge operation between a DataFrame and a Delta table.
The function supports update, delete, and insert operations on the target Delta table
based on conditions specified by the user. The function also supports partition pruning
to optimize the performance of the merge operation.

**Arguments**:

- `kwargs` - Parameters for the merge operation, passed to the MergeConfig class.
  

**Returns**:

  None
  

**Raises**:

- `EmptyDataframeException` - If the source dataframe is empty and ignore_empty_df is
  False.
- `ValueError` - If the key column is not set and the table does not have a primary key.
- `ValueError` - If the specified columns for update or insert do not exist in the DataFrame
  or are explicitly excluded from the merge operation.

<h4 id="delta_manager.DeltaManager.merge_dataframe_scd2">merge_dataframe_scd2</h4>

```python
@LoggingService.table_log_decorator(operation="merge_scd2")
def merge_dataframe_scd2(current_col_name: str = "SCD_IS_CURRENT",
                         start_date_col_name: str = "SCD_START_DATE",
                         end_date_col_name: str = "SCD_END_DATE",
                         **kwargs)
```

Merges the data in a spark DataFrame into a Delta table using SCD2 logic.

This function performs a merge operation between a DataFrame and a Delta table using SCD2 logic.
The function supports update, delete, and insert operations on the target Delta table based on
conditions specified by the user. The function also supports partition pruning to optimize the
performance of the merge operation.

**Arguments**:

- `current_col_name` _str_ - The name of the column in the Delta table that indicates whether a
  record is the current version of a row. Defaults to "SCD_IS_CURRENT".
- `start_date_col_name` _str_ - The name of the column in the Delta table that indicates the start
  date of a record. Defaults to "SCD_START_DATE".
- `end_date_col_name` _str_ - The name of the column in the Delta table that indicates the end date
  of a record. Defaults to "SCD_END_DATE".
- `extra_match_conditions` _str, optional_ - Additional conditions to be appended to the match
  conditions. Defaults to None.
- `kwargs` - Parameters for the merge operation, passed to the MergeConfig class.
  

**Returns**:

  None

<h4 id="delta_manager.DeltaManager.merge_dataframe_stream">merge_dataframe_stream</h4>

```python
@LoggingService.table_log_decorator(operation="merge")
def merge_dataframe_stream(table: Table,
                           data_frame: DataFrame,
                           checkpoint_location: str | None = None,
                           trigger: str = "availableNow",
                           trigger_specification: str | None = None,
                           key_columns: list[str] | None = None,
                           cols_to_update: list[str] | None = None,
                           cols_to_insert: list[str] | None = None,
                           cols_to_exclude: list[str] | None = None,
                           when_matched_update: bool = True,
                           when_matched_deleted: bool = False,
                           when_not_matched_insert: bool = True,
                           use_partition_pruning: bool = True,
                           ignore_empty_df: bool = False)
```

Merges the data in a spark DataFrame into a Delta table as a stream.

This function performs a merge operation between a DataFrame and a Delta table.
The function supports update, delete, and insert operations on the target Delta table
based on conditions specified by the user. The function also supports partition pruning
to optimize the performance of the merge operation.

**Arguments**:

- `table` _Table_ - A Table object representing the Delta table.
- `data_frame` _DataFrame_ - The DataFrame to be merged into the Delta table.
- `checkpoint_location` _str_ - Location of checkpoint. If None, defaults
  to the location of the table being written, with '_checkpoint_'
  added before name. Default None.
- `trigger` _str_ - Trigger. Default 'once', recommended to not change
  unless you know what you're doing.
- `trigger_specification` _str_ - Specification for chosen trigger (e.g.
  "5 seconds" for processingTime). Only useful for processingTime
  and continuous.
- `key_columns` _List[str], optional_ - List of column names that form the key for the merge
  operation. Defaults to the primary key of the table.
- `when_matched_update` _bool, optional_ - Flag to specify whether to perform an update
  operation when matching records are found in the target Delta table. Defaults to True.
- `when_matched_deleted` _bool, optional_ - Flag to specify whether to perform a delete
  operation when matching records are found in the target Delta table. Defaults to False.
- `when_not_matched_insert` _bool, optional_ - Flag to specify whether to perform an insert
  operation when matching records are not found in the target Delta table. Defaults to
  True.
- `cols_to_update` _List[str], optional_ - List of column names to be updated in the target
  Delta table. Defaults to columns of df.
- `cols_to_insert` _List[str], optional_ - List of column names to be inserted into the target
  Delta table. Defaults to columns of df.
- `cols_to_exclude` _List[str], optional_ - List of column names to be excluded from the merge
  operation. Defaults to None.
- `use_partition_pruning` _bool, optional_ - Flag to specify whether to use partition pruning to
  optimize the performance of the merge operation. Defaults to True.
- `ignore_empty_df` _bool, optional_ - A flag indicating whether to ignore an empty source
  dataframe. Defaults to False.
  

**Returns**:

  None
  

**Raises**:

- `EmptyDataframeException` - If the source dataframe is empty and ignore_empty_df is
  False.
- `ValueError` - If the key column is not set and the table does not have a primary key.
- `ValueError` - If the specified columns for update or insert do not exist in the DataFrame
  or are explicitly excluded from the merge operation.

<h4 id="delta_manager.DeltaManager.create_schema">create_schema</h4>

```python
def create_schema(catalog: str,
                  schema: str,
                  location: str,
                  comment: str = "Created by WinDEF DeltaManager") -> None
```

Creates a Schema in the catalog.

**Arguments**:

- `catalog` _str_ - The name of the catalog where the schema should be created.
- `schema` _str_ - The name of the schema to be created.
- `location` _str_ - The location where the schema should be stored.
- `comment` _str_ - The comment to be added to the schema. Defaults to "Created by WinDEF DeltaManager".
  

**Returns**:

  None

<h4 id="delta_manager.DeltaManager.create_table">create_table</h4>

```python
@LoggingService.table_log_decorator(operation="create")
def create_table(table: Table,
                 ignore_if_exists: bool = False,
                 properties: dict[str, Any] | None = None,
                 options: dict[str, Any] | None = None) -> None
```

Creates a Table in the catalog.

**Arguments**:

- `table` _Table_ - A Table object representing the Delta table.
- `ignore_if_exists` _bool, optional_ - If set to True, the function will return early
  without doing anything if the table already exists. Defaults to False.
- `properties` _dict, optional_ - Properties set on the table. Defaults to None.
- `options` _dict, optional_ - Table options. Defaults to None.
  

**Returns**:

  None

<h4 id="delta_manager.DeltaManager.shallow_clone_table">shallow_clone_table</h4>

```python
def shallow_clone_table(target_table: Table,
                        source_table: Table,
                        ignore_if_exists: bool = False) -> None
```

Clones a table using the shallow clone strategy.

**Arguments**:

- `target_table` _Table_ - A Table object representing the target table.
- `source_table` _Table_ - A Table object representing the source table.
- `ignore_if_exists` _bool, optional_ - If set to True, the function will return early
  without doing anything if the target table already exists. Defaults to False.
  

**Returns**:

  None

<h4 id="delta_manager.DeltaManager.delete_table">delete_table</h4>

```python
def delete_table(table: Table,
                 table_name: str,
                 delete_physical_data: bool = False)
```

Deletes a Table. For security reasons you are forced to pass the table_name.

If delete_physical_data is True the actually physical data on the ADLS will be deleted.
Use with caution!

**Arguments**:

- `table` _Table_ - A Table object representing the Delta table.
- `table_name` _str_ - Name of the table to be deleted. Required for security reasons.
- `delete_physical_data` _bool, optional_ - If set to True, deletes not only the metadata
  within the Catalog but also the physical data . Defaults to False.

<h4 id="delta_manager.DeltaManager.drop_table_from_catalog">drop_table_from_catalog</h4>

```python
@LoggingService.table_log_decorator(operation="drop_table_from_catalog")
def drop_table_from_catalog(table: Table) -> None
```

Removes a table from the catalog. Physical data is retained.

**Arguments**:

- `table` _Table_ - A Table object representing the Delta table.

<h1 id="schema_handler">schema_handler</h1>

<h2 id="schema_handler.SchemaHandler">SchemaHandler</h2>

```python
class SchemaHandler()
```

A class that handles operations related to schema.

**Attributes**:

- `spark` _SparkSession_ - A SparkSession instance for performing operations on schema.
- `contract_dir` _str_ - The directory where the data contract is stored.
- `environment` _str_ - The environment [DEV|TST|ACC|PRD].

<h4 id="schema_handler.SchemaHandler.__init__">__init__</h4>

```python
def __init__(contract_dir: str, environment: str)
```

Initializes a new instance of the SchemaHandler class.

**Arguments**:

- `contract_dir` _str_ - The directory where the data contract is stored.
- `environment` _str_ - The environment [DEV|TST|ACC|PRD].

<h4 id="schema_handler.SchemaHandler.create_tables_from_contract">create_tables_from_contract</h4>

```python
def create_tables_from_contract() -> None
```

Creates the tables defined in a data contract using a Spark Session.

<h4 id="schema_handler.SchemaHandler.get_tables">get_tables</h4>

```python
def get_tables() -> list[Table] | None
```

Get the tables for this data contract.

**Raises**:

- `ValueError` - If errors occur while reading the data contract.
- `ValueError` - If no schema could be instantiated from the data contract.
  

**Returns**:

- `List[Table]` - A list of Table instances for the data contract.

<h1 id="view_manager">view_manager</h1>

<h2 id="view_manager.ViewManager">ViewManager</h2>

```python
class ViewManager()
```

A class that manages Databricks views.

<h4 id="view_manager.ViewManager.create_view">create_view</h4>

```python
def create_view(table: Table,
                replace: bool = True,
                if_not_exists: bool = False,
                properties: dict[str, str] | None = None)
```

Creates a standardized SELECT ALL View for a given WinDEF Table.

TODO: RLS can be applied on the Table.
TODO: Is Column masking relevant?

**Arguments**:

- `table` _Table_ - The Table object to create the view for.
- `replace` _bool, optional_ - Replace view if exists. Defaults to True.
- `if_not_exists` _bool, optional_ - Create view if not exists. Defaults
  to False.
- `properties` _dict, optional_ - The properties of the table.
  

**Raises**:

- `ValueError` - When replace and if_not_exists are both true.

<h1 id="delta_operations">delta_operations</h1>

<h2 id="delta_operations.DeltaTableOperationType">DeltaTableOperationType</h2>

```python
class DeltaTableOperationType(Enum)
```

Mapping between Delta table operation types and their operation metric keys available in the Delta table history.

Values of metric keys included in this mapping are reported using the
logging capabilities of the Delta operations of the DeltaManager.

See https://docs.databricks.com/delta/history.html for a complete list and
description of available metrics for each operation type.

<h1 id="data_replication">data_replication</h1>

<h1 id="data_replication.data_replication_config">data_replication.data_replication_config</h1>

<h2 id="data_replication.data_replication_config.DataReplicationConfig">DataReplicationConfig</h2>

```python
class DataReplicationConfig(BaseModel)
```

A class to represent the configuration for data replication.

**Arguments**:

- `source_table_identifier` _str_ - The identifier of the source table.
- `target_environment` _str_ - The target environment, one of
  [dev, tst, acc].
- `target_table_identifier` _str_ - The identifier of the target table.
- `replication_strategy` _str_ - The mode of the replication, one of
  [delta, shallowclone].
- `mode` _str_ - The mode of the replication, one of [append, merge, overwrite].
- `delta_load_options` _DeltaLoadOptions | dict | str_ - Options for the
  delta loader strategy. This can be passed as a DeltaLoadOption, dict
  or string. The string can either be a YAML string that will be
  parsed using the `from_yaml_str` method of the DeltaLoadOptions
  class, or it can be a path on a Volume or Workspace directory to a
  YAML file that will be parsed using the `from_file` method.
- `filter_str` _str_ - A filter string to apply to the source table. Max
  length is 2048 characters due to limitations in dbutils.
- `merge_key_columns` _list[str]_ - The columns to merge on.
- `merge_cols_to_update` _list[str]_ - The columns to update.
- `merge_cols_to_insert` _list[str]_ - The columns to insert.
- `merge_cols_to_exclude` _list[str]_ - The columns to exclude.
- `merge_when_matched_update` _bool_ - Whether to update when matched.
- `merge_when_matched_delete` _bool_ - Whether to delete when matched.
- `merge_when_not_matched_insert` _bool_ - Whether to insert when not
  matched.
  

**Notes**:

  The target_table_identifier and target_environment are mutually
  exclusive. If the target_environment is provided, the
  target_table_identifier will be derived from the
  source_table_identifier.

<h4 id="data_replication.data_replication_config.DataReplicationConfig.parse_delta_load_options">parse_delta_load_options</h4>

```python
@model_validator(mode="before")
@classmethod
def parse_delta_load_options(cls, data: Any) -> Any
```

Parse delta load options and set custom defaults if neccessary.

<h4 id="data_replication.data_replication_config.DataReplicationConfig.validate_target">validate_target</h4>

```python
@model_validator(mode="before")
@classmethod
def validate_target(cls, data: Any) -> Any
```

Parse delta load options and set custom defaults if neccessary.

<h4 id="data_replication.data_replication_config.DataReplicationConfig.validate_delta_loader_config">validate_delta_loader_config</h4>

```python
@model_validator(mode="after")
def validate_delta_loader_config()
```

Validate the target configuration.

<h4 id="data_replication.data_replication_config.DataReplicationConfig.set_target_table_identifier">set_target_table_identifier</h4>

```python
@field_validator("target_table_identifier")
@classmethod
def set_target_table_identifier(cls, value)
```

Set the target_table_identifier.

<h4 id="data_replication.data_replication_config.DataReplicationConfig.set_target_environment">set_target_environment</h4>

```python
@field_validator("target_environment")
@classmethod
def set_target_environment(cls, value)
```

Set the target_environment.

<h4 id="data_replication.data_replication_config.DataReplicationConfig.validate_mode">validate_mode</h4>

```python
@field_validator("mode")
@classmethod
def validate_mode(cls, value)
```

Validate the mode.

<h4 id="data_replication.data_replication_config.DataReplicationConfig.validate_replication_strategy">validate_replication_strategy</h4>

```python
@field_validator("replication_strategy")
@classmethod
def validate_replication_strategy(cls, value)
```

Validate the mode.

<h4 id="data_replication.data_replication_config.DataReplicationConfig.validate_filter_str">validate_filter_str</h4>

```python
@field_validator("filter_str")
@classmethod
def validate_filter_str(cls, value)
```

Validate the mode.

<h4 id="data_replication.data_replication_config.DataReplicationConfig.from_widgets">from_widgets</h4>

```python
@classmethod
def from_widgets(cls)
```

Create a DataReplicationConfig instance from the Databricks widgets.

<h4 id="data_replication.data_replication_config.DataReplicationConfig.setup_widgets">setup_widgets</h4>

```python
@staticmethod
def setup_widgets()
```

Setup the Databricks widgets.

<h1 id="data_replication.data_replication_service">data_replication.data_replication_service</h1>

<h2 id="data_replication.data_replication_service.DataReplicationService">DataReplicationService</h2>

```python
class DataReplicationService()
```

A service to replicate data from one table to another.

The DataReplicationService is used to replicate data from one table to
another. It can be used to replicate data from one environment to another,
or to replicate data from one table to another within the same environment.
The service supports different modes of replication, such as append and
merge, and allows for filtering and timestamp-based replication.

If a target table already exists, the service will update the target table
with the latest data from the source table. If the target table does not
exist, the service will create the target table and load the data from the
source table.

<h4 id="data_replication.data_replication_service.DataReplicationService.replicate_table">replicate_table</h4>

```python
def replicate_table(config: DataReplicationConfig | None = None,
                    delta_loader: DeltaLoader | None = None)
```

Replicate the target table with the source table.

If the table was already replicated, it will update the target table
otherwise it will clone the source table to the target table.

**Arguments**:

- `config` _optional[DataReplicationConfig]_ - The configuration for the data
  replication stream.
- `delta_loader` _optional[DeltaCDFLoader]_ - The DeltaCDFLoader to use for dependency injection.
  

**Raises**:

- `ValueError` - If the source table does not exist.
- `ValueError` - If the source table location is not set.

<h1 id="writer">writer</h1>

<h1 id="writer.writer">writer.writer</h1>

<h2 id="writer.writer.WinDEFDataFrameWriter">WinDEFDataFrameWriter</h2>

```python
class WinDEFDataFrameWriter(ABC)
```

Dataframe Writer class to write data.

<h4 id="writer.writer.WinDEFDataFrameWriter.write_stream">write_stream</h4>

```python
@abstractmethod
def write_stream(**kwargs: Any)
```

Writes a data frame stream.

<h4 id="writer.writer.WinDEFDataFrameWriter.write">write</h4>

```python
@abstractmethod
def write(data_frame: DataFrame, **kwargs: Any)
```

Writes a data frame.

<h4 id="writer.writer.WinDEFDataFrameWriter.log_operation">log_operation</h4>

```python
def log_operation(operation: str,
                  identifier: str,
                  status: str,
                  error: str = "")
```

Logs the metrics for one operation on the given identifier.

**Arguments**:

- `operation` _str_ - Describes the type of operation, e.g. 'read_api'.
- `identifier` _str_ - An identifier for the object that's being interacted with.
- `status` _str_ - The status of the operation. Must be one of "start", "failed", "succeeded".
- `error` _str_ - The error message, if any. Defaults to ''.

<h1 id="writer.table_writer">writer.table_writer</h1>

<h2 id="writer.table_writer.TableDataFrameWriter">TableDataFrameWriter</h2>

```python
class TableDataFrameWriter(WinDEFDataFrameWriter)
```

Utility class for writing a DataFrame to a Delta Table.

<h4 id="writer.table_writer.TableDataFrameWriter.write_stream">write_stream</h4>

```python
def write_stream(data_frame: DataFrame | None = None,
                 table_name: str | None = None,
                 checkpoint_location: str | None = None,
                 partition_cols: list[str] | None = None,
                 merge_schema: bool = True,
                 mode: str = "append",
                 trigger: str = "availableNow",
                 trigger_specification: str | None = None,
                 options: dict[str, Any] | None = None,
                 **_: Any)
```

Writes a dataframe to specified location in specified format as a stream.

**Arguments**:

- `data_frame` _DataFrame_ - Dataframe to write
- `table_name` _str_ - Delta Table to write data to.
- `format` _str_ - Format of files to read. Default 'delta'.
- `checkpoint_location` _str_ - Location of checkpoint. Defaults to
  location of table being written, with '_checkpoint_' added
  before name. Default None.
- `partition_cols` _list_ - Columns to partition on. Default None, but
  highly recommended for any medium and larger datasets.
- `merge_schema` _bool_ - Specifies whether or not to merge schema of
  existing table at location (if any). Default True.
- `mode` _str_ - Specifies how data of a streaming DataFrame/Dataset is
  written to a streaming sink. Default 'append'.
- `trigger` _str_ - Trigger. Default 'availableNow', recommended to not
  change unless you know what you're doing.
- `trigger_specification` _str_ - Specification for chosen trigger (e.g.
  "5 seconds" for processingTime). Only useful for processingTime
  and continuous.
- `options` _dict_ - Additional dataframe writer options. Default None.
  

**Raises**:

- `ValueError` - If location or data_frame is not provided.

<h4 id="writer.table_writer.TableDataFrameWriter.write">write</h4>

```python
def write(data_frame: DataFrame,
          table_name: str | None = None,
          partition_cols: list[str] | None = None,
          mode: str = "append",
          options: dict[str, Any] | None = None,
          **_: Any)
```

Writes a dataframe to specified table.

**Arguments**:

- `data_frame` _DataFrame_ - Dataframe to write
- `table_name` _str_ - Name of the table to write data to.
- `format` _str_ - Format of files to write. Default 'delta'.
- `partition_cols` _list_ - Columns to partition on. Default None, but highly recommended
  for any medium and larger datasets.
- `mode` _str_ - Specifies the behavior when data or table already exists. Default 'append'.
- `options` _dict_ - Additional dataframe writer options. Default None.
  
  Modes:
  * `append`: Append contents of this DataFrame to existing data.
  * `overwrite`: Overwrite existing data.
  * `error` or `errorifexists`: Throw an exception if data already exists.
  * `ignore`: Silently ignore this operation if data already exists.
  

**Raises**:

- `ValueError` - If table_name is not provided.

<h1 id="writer.kafka_writer">writer.kafka_writer</h1>

<h2 id="writer.kafka_writer.KafkaDataFrameWriter">KafkaDataFrameWriter</h2>

```python
class KafkaDataFrameWriter(WinDEFDataFrameWriter)
```

Utility class for writing a DataFrame to a Kafka Endpoint.

<h4 id="writer.kafka_writer.KafkaDataFrameWriter.write_stream">write_stream</h4>

```python
def write_stream(data_frame: DataFrame | None = None,
                 kafka_endpoint: str | None = None,
                 kafka_topic: str | None = None,
                 client_id: str | None = None,
                 client_secret: str | None = None,
                 kafka_endpoint_port: int = 9093,
                 trigger: str = "availableNow",
                 trigger_specification: str | None = None,
                 options: dict[str, str] | None = None,
                 **_: Any)
```

Writes a dataframe to a Kafka endpoint as a stream.

**Arguments**:

- `data_frame` _DataFrame_ - Spark Dataframe
- `kafka_endpoint` _str_ - Kafka server endpoint from where to read.
- `kafka_topic` _str_ - Kafka topic to read.
- `client_id` _str_ - Client Id of the message reader service principal.
- `client_secret` _str_ - Client secret of the message reader service principal.
- `kafka_endpoint_port` _int_ - Port of the Kafka server endpoint. Defaults to the event hub Kafka port 9093.
- `trigger` _str_ - Trigger. Default 'availableNow', recommended to not change unless you know what you're doing.
- `trigger_specification` _str_ - Specification for chosen trigger (e.g. "5 seconds" for processingTime). Only
  useful for processingTime and continuous.
- `options` _dict_ - Additional options passed to the dataframe.
  

**Raises**:

- `ValueError` - If data_frame, kafka_endpoint, kafka_topic, client_id, or client_secret are not provided.
- `ValueError` - If trigger is not implemented.

<h4 id="writer.kafka_writer.KafkaDataFrameWriter.write">write</h4>

```python
def write(data_frame: DataFrame,
          kafka_endpoint: str | None = None,
          kafka_topic: str | None = None,
          client_id: str | None = None,
          client_secret: str | None = None,
          kafka_endpoint_port: int = 9093,
          options: dict[str, str] | None = None,
          **_: Any)
```

Writes a dataframe to a Kafka endpoint.

**Arguments**:

- `data_frame` _DataFrame_ - Spark Dataframe
- `kafka_endpoint` _str_ - Kafka server endpoint from where to read.
- `kafka_topic` _str_ - Kafka topic to read.
- `client_id` _str_ - Client Id of the message reader service principal.
- `client_secret` _str_ - Client secret of the message reader service principal.
- `kafka_endpoint_port` _int_ - Port of the Kafka server endpoint. Defaults to the event hub Kafka port 9093.
- `options` _dict_ - Additional options passed to the dataframe.
  

**Raises**:

- `ValueError` - If data_frame, kafka_endpoint, kafka_topic, client_id, or client_secret are not provided.

<h1 id="writer.file_writer">writer.file_writer</h1>

<h2 id="writer.file_writer.FileDataFrameWriter">FileDataFrameWriter</h2>

```python
class FileDataFrameWriter(WinDEFDataFrameWriter)
```

Utility class for writing a DataFrame to a file.

<h4 id="writer.file_writer.FileDataFrameWriter.write_stream">write_stream</h4>

```python
def write_stream(data_frame: DataFrame | None = None,
                 location: str | None = None,
                 format: str = "delta",
                 checkpoint_location: str | None = None,
                 partition_cols: list[str] | None = None,
                 merge_schema: bool = True,
                 mode: str = "append",
                 trigger: str = "availableNow",
                 trigger_specification: str | None = None,
                 options: dict[str, Any] | None = None,
                 **_: Any)
```

Writes a dataframe to specified location in specified format as a stream.

**Arguments**:

- `data_frame` _DataFrame_ - Dataframe to write
- `location` _str_ - Location to write data to.
- `format` _str_ - Format of files to read. Default 'delta'.
- `checkpoint_location` _str_ - Location of checkpoint. Defaults to
  location of table being written, with '_checkpoint_' added
  before name. Default None.
- `partition_cols` _list_ - Columns to partition on. Default None, but
  highly recommended for any medium and larger datasets.
- `merge_schema` _bool_ - Specifies whether or not to merge schema of
  existing table at location (if any). Default True.
- `mode` _str_ - Specifies how data of a streaming DataFrame/Dataset is
  written to a streaming sink. Default 'append'.
- `trigger` _str_ - Trigger. Default 'availableNow', recommended to not
  change unless you know what you're doing.
- `trigger_specification` _str_ - Specification for chosen trigger (e.g.
  "5 seconds" for processingTime). Only useful for processingTime
  and continuous.
- `options` _dict_ - Additional dataframe writer options. Default None.
  

**Raises**:

- `ValueError` - If location or data_frame is not provided.

<h4 id="writer.file_writer.FileDataFrameWriter.write">write</h4>

```python
def write(data_frame: DataFrame,
          location: str | None = None,
          format: str = "delta",
          partition_cols: list[str] | None = None,
          mode: str = "append",
          options: dict[str, Any] | None = None,
          **_: Any)
```

Writes a dataframe to specified location in specified format.

**Arguments**:

- `data_frame` _DataFrame_ - Dataframe to write
- `location` _str_ - Location to write data to.
- `format` _str_ - Format of files to write. Default 'delta'.
- `partition_cols` _list_ - Columns to partition on. Default None, but highly recommended
  for any medium and larger datasets.
- `mode` _str_ - Specifies the behavior when data or table already exists. Default 'append'.
- `options` _dict_ - Additional dataframe writer options. Default None.
  
  Modes:
  * `append`: Append contents of this DataFrame to existing data.
  * `overwrite`: Overwrite existing data.
  * `error` or `errorifexists`: Throw an exception if data already exists.
  * `ignore`: Silently ignore this operation if data already exists.
  

**Raises**:

- `ValueError` - If location is not provided.

<h1 id="reader">reader</h1>

<h1 id="reader.api_reader">reader.api_reader</h1>

<h2 id="reader.api_reader.APIReader">APIReader</h2>

```python
class APIReader(WinDEFDataFrameReader)
```

Utility class for reading an API.

**Arguments**:

- `base_url` _str_ - The base URL of the API
- `auth` _AuthBase_ - The basic authentication for the API. E.g. taken from windef.api_client.auth
  or requests.
  default_headers dict[str, str]: Headers that will be attached to every request. Defaults to None.
- `enable_logging_to_azure` _bool_ - If enabled, logging will be sent to the Log Analytics Workspace.
  Defaults to None.

<h4 id="reader.api_reader.APIReader.read">read</h4>

```python
def read(endpoint: str = "",
         method: str = "GET",
         key: str | None = None,
         timeout: int = 30,
         params: dict[str, str] | None = None,
         headers: dict[str, str] | None = None,
         data: dict[str, str] | None = None,
         json_body: dict[str, str] | None = None,
         max_retries: int = 0,
         options: dict[str, str] | None = None,
         add_metadata_column: bool = False,
         backoff_factor: int = 1,
         save_path: str | None = None,
         **_: Any) -> DataFrame
```

Reads messages from an API endpoint and returns DataFrame.

**Arguments**:

- `endpoint` _str_ - The URL where the request is sent.
- `method` _str, optional_ - The HTTP method the request uses. Defaults to GET.
- `key` _str_ - The name of the data field retrieved from the API response. Defaults to None.
- `timeout` _int, optional_ - The number of seconds the client will wait for the server to send a response.
  Defaults to 30.
- `params` _dict[str, str], optional_ - Optional parameters to be sent with the request. Defaults to None.
- `headers` _dict[str, str], optional_ - Headers to be used in the request. Defaults to None.
- `data` _dict[str, str], optional_ - The data to be sent with the request. Defaults to None.
- `json_body` _dict[str, str], optional_ - The JSON data to be sent with the request. Defaults to None.
- `max_retries` _int, optional_ - The maximum number of retries for the request. Defaults to 0.
- `options` _dict[str, str], optional_ - Spark dataframe reader options. Defaults to None.
- `backoff_factor` _int_ - Factor for exponential backoff between retries.
- `add_metadata_column` _bool_ - If set, adds a __metadata column
  containing metadata about the API response.
- `save_path` _str_ - The path to save the response as JSON file to. Defaults to None.
  

**Raises**:

- `ValueError` - If endpoint is not provided.
- `ValueError` - If the save_path is a directory instead of a file path.
  

**Returns**:

- `DataFrame` - A DataFrame containing the data from the API response.

<h4 id="reader.api_reader.APIReader.read_stream">read_stream</h4>

```python
def read_stream(**_: Any) -> DataFrame
```

Currently not implemented, requires async API client.

<h1 id="reader.file_reader">reader.file_reader</h1>

<h2 id="reader.file_reader.FileDataFrameReader">FileDataFrameReader</h2>

```python
class FileDataFrameReader(WinDEFDataFrameReader)
```

Utility class for reading a file into a DataFrame.

<h4 id="reader.file_reader.FileDataFrameReader.read_stream">read_stream</h4>

```python
def read_stream(location: str = "",
                schema: str | dict[str, str] | None = None,
                format: str = "delta",
                include_source_file_column: bool = False,
                options: dict[str, Any] | None = None,
                **_: Any) -> DataFrame
```

Reads specified location as a stream and returns streaming DataFrame.

**Arguments**:

- `location` _str_ - Location of files to read.
- `format` _str_ - Format of files to read.
- `schema` _dict_ - Schema of the file.
- `include_source_file_column` _bool_ - Decides if the column
  `_source_file` is included, containing the file, where the data
  was read from. Defaults to False.
- `options` _dict_ - Spark DataFrame reader options.
  

**Raises**:

- `ValueError` - If location is not provided.
  

**Returns**:

- `DataFrame` - Streaming DataFrame.

<h4 id="reader.file_reader.FileDataFrameReader.read">read</h4>

```python
def read(location: str = "",
         format: str = "delta",
         schema: str | dict[str, str] | None = None,
         include_source_file_column: bool = False,
         options: dict[str, Any] | None = None,
         **_: Any) -> DataFrame
```

Reads specified location and returns DataFrame.

**Arguments**:

- `location` _str_ - Location of files to read.
- `format` _str_ - Format of files to read.
- `schema` _str_ - Schema of the file.
- `include_source_file_column` _bool_ - Decides if the column
  `_source_file` is included, containing the file, where the data
  was read from. Defaults to False.
- `options` _dict_ - Spark DataFrame reader options.
  

**Raises**:

- `ValueError` - If location is not provided.
  

**Returns**:

- `DataFrame` - The DataFrame that was read.

<h4 id="reader.file_reader.FileDataFrameReader.read_by_extension">read_by_extension</h4>

```python
def read_by_extension(location: str,
                      extension: str,
                      schema: str | dict[str, str] | None = None,
                      search_subdirs: bool = True,
                      include_source_file_column: bool = False,
                      options: dict[str, Any] | None = None) -> DataFrame
```

Reads specified location and returns DataFrame based on extension provided.

Parses top level and sub level directories by default.

**Arguments**:

- `location` _str_ - Location of files to read.
- `schema` _dict_ - Schema of the file.
- `extension` _str_ - Supported File extensions: 'csv', 'json',
  'parquet', 'txt.
- `search_subdirs` _bool_ - Specifies whether or not to include files in
  subdirectories of location provided. Defaults to True.
- `include_source_file_column` _bool_ - Decides if the column
  `_source_file` is included, containing the file, where the data
  was read from. Defaults to False.
- `options` _dict_ - Spark DataFrame reader options.

<h4 id="reader.file_reader.FileDataFrameReader.add_source_file_column">add_source_file_column</h4>

```python
def add_source_file_column(df: DataFrame) -> DataFrame
```

Add source file column to the read DataFrame.

<h1 id="reader.volume_reader">reader.volume_reader</h1>

<h2 id="reader.volume_reader.VolumeReader">VolumeReader</h2>

```python
class VolumeReader()
```

Databricks Volume Reader class to read files from a volume.

**Arguments**:

  Logger currently broken, implement when fixed.

<h4 id="reader.volume_reader.VolumeReader.read_file">read_file</h4>

```python
def read_file(location: str, fail_on_error: bool = True) -> str | None
```

Return bytes read from a file.

**Arguments**:

- `location` _str_ - Path to the file on the volume
- `fail_on_error` _bool_ - If True, raise an exception on error.
  If False, return None on error. Defaults to True.
  

**Returns**:

- `str` - The content of the file.

<h4 id="reader.volume_reader.VolumeReader.read_files">read_files</h4>

```python
def read_files(files: list[str],
               fail_on_error: bool = True) -> list[str | None]
```

Return a list of file contents.

**Arguments**:

- `files` _str_ - A list of file paths.
- `fail_on_error` _bool_ - If True, raise an exception on error.
  If False, return None on error. Defaults to True.
  

**Returns**:

- `list[str|None]` - A list of file contents. Can be None if an error
  occurred and fail_on_error is set to False.

<h4 id="reader.volume_reader.VolumeReader.ls">ls</h4>

```python
def ls(location: str, recursive: bool = False) -> list[str]
```

Lists all files in a directory.

**Arguments**:

- `location` _str_ - Path to the directory on the volume.
- `recursive` _bool_ - recursively go through directories.

<h4 id="reader.volume_reader.VolumeReader.log_operation">log_operation</h4>

```python
def log_operation(operation: str,
                  identifier: str,
                  status: str,
                  error: str = "")
```

Logs the metrics for one operation on the given identifier.

**Arguments**:

- `operation` _str_ - Describes the type of operation, e.g. 'read_api'.
- `identifier` _str_ - An identifier for the object that's being interacted with.
- `status` _str_ - The status of the operation. Must be one of "start", "failed", "succeeded".
- `error` _str_ - The error message, if any. Defaults to ''.

<h1 id="reader.reader">reader.reader</h1>

<h2 id="reader.reader.WinDEFDataFrameReader">WinDEFDataFrameReader</h2>

```python
class WinDEFDataFrameReader(ABC)
```

Dataframe Reader class to build a spark dataframe.

<h4 id="reader.reader.WinDEFDataFrameReader.read_stream">read_stream</h4>

```python
@abstractmethod
def read_stream(**kwargs) -> DataFrame
```

Return a streaming data frame.

<h4 id="reader.reader.WinDEFDataFrameReader.read">read</h4>

```python
@abstractmethod
def read(**kwargs) -> DataFrame
```

Return a batch data frame.

<h4 id="reader.reader.WinDEFDataFrameReader.log_operation">log_operation</h4>

```python
def log_operation(operation: str,
                  identifier: str,
                  status: str,
                  error: str = "")
```

Logs the metrics for one operation on the given identifier.

**Arguments**:

- `operation` _str_ - Describes the type of operation, e.g. 'read_api'.
- `identifier` _str_ - An identifier for the object that's being interacted with.
- `status` _str_ - The status of the operation. Must be one of "start", "failed", "succeeded".
- `error` _str_ - The error message, if any. Defaults to ''.

<h1 id="reader.kafka_reader">reader.kafka_reader</h1>

<h2 id="reader.kafka_reader.KafkaDataFrameReader">KafkaDataFrameReader</h2>

```python
class KafkaDataFrameReader(WinDEFDataFrameReader)
```

Utility class for reading from a Kafka API into a DataFrame.

<h4 id="reader.kafka_reader.KafkaDataFrameReader.read_stream">read_stream</h4>

```python
def read_stream(kafka_endpoint: str = "",
                kafka_topic: str = "",
                client_id: str = "",
                client_secret: str = "",
                kafka_endpoint_port: int = 9093,
                options: dict[str, str] | None = None,
                **_: Any) -> DataFrame
```

Reads messages from a Kafka endpoint as a stream and returns streaming DataFrame.

**Arguments**:

- `kafka_endpoint` _str_ - Kafka server endpoint from where to read.
- `kafka_topic` _str_ - Kafka topic to read.
- `client_id` _str_ - Client Id of the message reader service principal.
- `client_secret` _str_ - Client secret of the message reader service principal.
- `kafka_endpoint_port` _int_ - Port of the Kafka server endpoint. Defaults to the event hub Kafka port 9093.
- `options` _dict_ - Additional options passed to the dataframe.
  

**Raises**:

- `ValueError` - If Kafka endpoint, topic, client_id, or client_secret is not provided.
  

**Returns**:

- `DataFrame` - A streaming DataFrame containing the data from the Kafka topic.

<h4 id="reader.kafka_reader.KafkaDataFrameReader.read">read</h4>

```python
def read(kafka_endpoint: str = "",
         kafka_topic: str = "",
         client_id: str = "",
         client_secret: str = "",
         kafka_endpoint_port: int = 9093,
         options: dict[str, str] | None = None,
         **_: Any) -> DataFrame
```

Reads messages from a Kafka endpoint and returns DataFrame.

**Arguments**:

- `kafka_endpoint` _str_ - Kafka server endpoint from where to read.
- `kafka_topic` _str_ - Kafka topic to read.
- `client_id` _str_ - Client Id of the message reader service principal.
- `client_secret` _str_ - Client secret of the message reader service principal.
- `kafka_endpoint_port` _int_ - Port of the Kafka server endpoint. Defaults to the event hub Kafka port 9093.
- `options` _dict_ - Additional options passed to the dataframe.
  

**Raises**:

- `ValueError` - If Kafka endpoint, topic, client_id, or client_secret is not provided.
  

**Returns**:

- `DataFrame` - A DataFrame containing the data from the Kafka topic.

<h1 id="reader.table_reader">reader.table_reader</h1>

<h2 id="reader.table_reader.TableDataFrameReader">TableDataFrameReader</h2>

```python
class TableDataFrameReader(WinDEFDataFrameReader)
```

Utility class for reading a Delta table into a DataFrame.

<h4 id="reader.table_reader.TableDataFrameReader.read_stream">read_stream</h4>

```python
def read_stream(table_name: str = "",
                options: dict[str, Any] | None = None,
                **_: Any) -> DataFrame
```

Reads specified Delta table as a stream and returns streaming DataFrame.

**Arguments**:

- `table_name` _str_ - Name of the table to read.
- `options` _dict_ - Spark dataframe reader options.
  

**Raises**:

- `ValueError` - If table_name is not provided.
  

**Returns**:

- `DataFrame` - Streaming DataFrame.

<h4 id="reader.table_reader.TableDataFrameReader.read">read</h4>

```python
def read(table_name: str = "",
         options: dict[str, Any] | None = None,
         delta_load_options: DeltaLoadOptions | None = None,
         **_: Any) -> DataFrame
```

Reads specified Delta table and returns DataFrame.

**Arguments**:

- `table_name` _str_ - Name of Delta table to read.
- `options` _dict_ - Spark dataframe reader options.
- `delta_load_options` _dict_ - Delta load options.
  

**Raises**:

- `ValueError` - If table_name is not provided.
  

**Returns**:

- `DataFrame` - DataFrame.

<h1 id="reader.excel_reader">reader.excel_reader</h1>

<h2 id="reader.excel_reader.ExcelDataFrameReader">ExcelDataFrameReader</h2>

```python
class ExcelDataFrameReader(WinDEFDataFrameReader)
```

Utility class for reading an Excel file into a DataFrame.

This class uses the Pandas API on Spark to read Excel files to a DataFrame.
More information can be found in the [official
documentation](https://spark.apache.org/docs/latest/api/python/reference/pyspark.pandas/index.html).

<h4 id="reader.excel_reader.ExcelDataFrameReader.read_stream">read_stream</h4>

```python
def read_stream(**_: Any) -> DataFrame
```

Currently not implemented.

<h4 id="reader.excel_reader.ExcelDataFrameReader.read">read</h4>

```python
def read(*,
         location: str = "",
         sheet_name: str | int | list = 0,
         sheet_name_as_column: bool = False,
         header: int | list[int] = 0,
         index_col: int | list[int] | None = None,
         usecols: int | str | list | Callable | None = None,
         dtype: str | None = None,
         fillna: str | dict[str, list[str]] | dict[str, str] | None = None,
         true_values: list[Any] | None = None,
         false_values: list[Any] | None = None,
         nrows: int | None = None,
         na_values: str | list[str] | dict[str, list[str]] | dict[str, str]
         | None = None,
         keep_default_na: bool = True,
         parse_dates: bool | list | dict = False,
         date_parser: Callable | None = None,
         thousands: str | None = None,
         include_index: bool = False,
         options: dict | None = None,
         **_: Any) -> DataFrame
```

Reads Excel file on specified location and returns DataFrame.

**Arguments**:

- `location` _str_ - Location of files to read.
- `sheet_name` _str|int|list_ - Strings are used for sheet names.
  Integers are used in zero-indexed sheet positions. Lists of
  strings/integers are used to request multiple sheets. Specify None
  to get all sheets. Defaults to 0.
- `sheet_name_as_column` _bool_ - Add a column containing the sheet_name.
  Only works if sheet_name is specified. Defaults to False.
- `header` _header: int|list[int]_ - Row to use for column labels. If a
  list of integers is passed those row positions will be combined. Use
  None if there is no header. Defaults to 0.
- `index_col` _int|list[int]_ - Column to use as the row labels of the
  DataFrame. Pass None if there is no such column. If a list is
  passed, those columns will be combined. Defaults to None.
- `usecols` _int|str|list|Callable_ - Return a subset of the columns. If
  None, then parse all columns. If str, then indicates comma separated
  list of Excel column letters and column ranges (e.g. “A:E” or
  “A,C,E:F”). Ranges are inclusive of both sides. nIf list of int,
  then indicates list of column numbers to be parsed. If list of
  string, then indicates list of column names to be parsed. If
  Callable, then evaluate each column name against it and parse the
  column if the Callable returns True. Defaults to None.
- `dtype` _str|dict[str,str]_ - Data type for data or columns. Defaults to None.
- `fillna` _str|dict[str,list[str]]|dict[str, str]_ - If specified, fills
  NaN / Null values in columns using the specified fillna method.
  Defaults to None.
- `true_values` _list_ - Values to consider as True. Defaults to None.
- `false_values` _list_ - Values to consider as False. Defaults to None.
- `nrows` _int_ - Number of rows to parse. Defaults to None.
- `na_values` _list[str]|dict[str]_ - Additional strings to recognize as
  NA/NaN. If dict passed, specific per-column NA values. Defaults to
  None.
- `keep_default_na` _bool_ - If na_values are specified and
  keep_default_na is False the default NaN values are overridden,
  otherwise they're appended to. Defaults to True.
- `parse_dates` _bool, list, dict_ - The behavior is as follows:
  - bool. If True -> try parsing the index.
  - list of int or names. e.g. If [1, 2, 3] -> try parsing columns 1, 2, 3 each as a separate date column.
  - list of lists. e.g. If [[1, 3]] -> combine columns 1 and 3 and parse as a single date column.
  - dict, e.g. {{"foo" : [1, 3]}} -> parse columns 1, 3 as date and call result "foo"
  If a column or index contains an unparseable date, the entire
  column or index will be returned unaltered as an object data
  type. Defaults to False.
- `date_parser` _function_ - Function to use for converting a sequence of
  string columns to an array of datetime instances. The default uses
  dateutil.parser.parser to do the conversion.
- `thousands` _str_ - Thousands separator for parsing string columns to
  numeric. Note that this parameter is only necessary for columns
  stored as TEXT in Excel, any numeric columns will automatically be
  parsed, regardless of display format. Defaults to None.
- `include_index` _bool_ - Include an index column. The column will be
  named `_index`.
- `options` _dict_ - Optional keyword arguments passed to
  pyspark.pandas.read_excel and handed to TextFileReader. Defaults to
  None.
  

**Raises**:

- `ValueError` - If location is not provided.
  

**Returns**:

- `DataFrame` - A DataFrame containing the data from the Excel file.

<h1 id="delta_loader">delta_loader</h1>

<h1 id="delta_loader.delta_loader_metadata_table">delta_loader.delta_loader_metadata_table</h1>

<h2 id="delta_loader.delta_loader_metadata_table.DeltaLoaderMetadataTable">DeltaLoaderMetadataTable</h2>

```python
class DeltaLoaderMetadataTable(Table)
```

A Table Model for the Delta CDF Reader Metadata Table.

<h1 id="delta_loader.delta_loader_factory">delta_loader.delta_loader_factory</h1>

<h4 id="delta_loader.delta_loader_factory.consume_delta_load">consume_delta_load</h4>

```python
def consume_delta_load(runtime_info: dict[str, Any],
                       delta_load_identifier: str | None = None) -> None
```

Consumes a delta load by updating the metadata table.

**Arguments**:

- `runtime_info` _dict_ - Runtime information.
- `delta_load_identifier` _str, optional_ - If set, the
  ConsumeDeltaLoadAction action will only consume DeltaLoader
  transaction for the given delta_load_identifier. Defaults to None.

<h2 id="delta_loader.delta_loader_factory.DeltaLoadOptions">DeltaLoadOptions</h2>

```python
class DeltaLoadOptions(BaseModel)
```

Options to configure the DeltaLoader.

**Arguments**:

- `strategy` _str_ - delta load strategy to use.
- `delta_load_identifier` _str_ - Unique delta load identifier used to track
  the delta load metadata.
- `strategy_options` _dict_ - Options used to configure the chosen delta load
  strategy. See the config class of the particular strategy for more
  info.
- `metadata_table_identifier` _str_ - Identifier of the metadata table used
  to keep track of the delta load metadata. The table will be created
  if it does not exist. If none, it will default to
  `<source_catalog>.<source_schema>.metadata_delta_load`.

<h4 id="delta_loader.delta_loader_factory.DeltaLoadOptions.from_yaml_str">from_yaml_str</h4>

```python
@classmethod
def from_yaml_str(cls, yaml_str: str) -> Self
```

Creates an instance of DeltaLoadOptions from a YAML string.

<h4 id="delta_loader.delta_loader_factory.DeltaLoadOptions.from_file">from_file</h4>

```python
@classmethod
def from_file(cls, path: str | Path) -> Self
```

Creates an instance of DeltaLoadOptions from a YAML file.

<h2 id="delta_loader.delta_loader_factory.DeltaLoaderFactory">DeltaLoaderFactory</h2>

```python
class DeltaLoaderFactory()
```

Factory to create a DeltaLoader instance based on the DeltaLoadOptions.

<h4 id="delta_loader.delta_loader_factory.DeltaLoaderFactory.create_loader">create_loader</h4>

```python
@staticmethod
def create_loader(table_identifier: str,
                  options: DeltaLoadOptions) -> DeltaLoader
```

Creates an instance of DeltaLoader, choosing the desired strategy.

<h1 id="delta_loader.delta_loader">delta_loader.delta_loader</h1>

<h2 id="delta_loader.delta_loader.DeltaLoader">DeltaLoader</h2>

```python
class DeltaLoader(ABC)
```

Base class for delta load operations.

**Arguments**:

- `table_identifier` _str_ - Identifier for the table to be loaded.
- `delta_load_identifier` _str_ - Identifier for the delta load.
- `metadata_table_identifier` _str | None, optional_ - Identifier for the
  metadata table. If None, the metadata_table_identifier will be
  derived from the table identifier:
  `<table_catalog>.<table_schema>.metadata_delta_load`.

<h4 id="delta_loader.delta_loader.DeltaLoader.read_data">read_data</h4>

```python
@abstractmethod
def read_data(options: dict[str, str] | None = None) -> DataFrame
```

Reads data incrementally using a strategy.

**Arguments**:

  options(dict[str, str], optional): Additional DataFrameReader
  options.

<h4 id="delta_loader.delta_loader.DeltaLoader.verify">verify</h4>

```python
@abstractmethod
def verify() -> None
```

Verify that the source table qualifies for the delta load strategy.

<h4 id="delta_loader.delta_loader.DeltaLoader.reset_cdf">reset_cdf</h4>

```python
def reset_cdf() -> None
```

Invalidates all changes in the metadata for the delta load.

<h4 id="delta_loader.delta_loader.DeltaLoader.consume_data">consume_data</h4>

```python
def consume_data() -> None
```

Marks data as consumed in the metadata for the delta load.

<h4 id="delta_loader.delta_loader.DeltaLoader.write_data">write_data</h4>

```python
def write_data(write_callable: partial)
```

Wrapper to write and consume a delta load.

<h1 id="delta_loader.strategies.delta_cdf_loader">delta_loader.strategies.delta_cdf_loader</h1>

<h2 id="delta_loader.strategies.delta_cdf_loader.DeltaCDFConfig">DeltaCDFConfig</h2>

```python
class DeltaCDFConfig(BaseModel)
```

This class holds the config for the DeltaCDFLoader.

**Arguments**:

- `deduplication_columns` _list[str | Column]_ - A list of columns used for
  deduplication.
- `from_commit_version` _int | None_ - The starting commit version. If None,
  it starts from the first viable version.
- `to_commit_version` _int | None_ - The ending commit version. If None, it
  goes up to the latest version.
- `enable_full_load` _bool_ - Enables an initial full load of the target
  table. If no valid delta load history for the table exists, the
  delta loader will do a full load of the target table and set the
  metadata to the newest commit version. This might be useful if the
  change data feed history is incomplete, either because the table was
  vacuumed or the change data feed was enabled later in the lifecycle
  of the table. Otherwise the table will initially be loaded from the
  first valid commit version. When True, `from_commit_version` and
  `to_commit_version` will be ignored on the initial load. Defaults to
  False.

<h2 id="delta_loader.strategies.delta_cdf_loader.DeltaCDFLoader">DeltaCDFLoader</h2>

```python
class DeltaCDFLoader(DeltaLoader)
```

Implementation of the DeltaLoader interface using CDF strategy.

**Arguments**:

- `config` _DeltaCDFConfig_ - Configuration for the DeltaCDFLoader.
- `table_identifier` _str_ - Identifier for the table to be loaded.
- `delta_load_identifier` _str_ - Identifier for the delta load.
- `metadata_table_identifier` _str | None, optional_ - Identifier for the
  metadata table. Defaults to None.

<h4 id="delta_loader.strategies.delta_cdf_loader.DeltaCDFLoader.verify">verify</h4>

```python
def verify() -> None
```

Verify that the source table has the Change Data Feed enabled.

<h4 id="delta_loader.strategies.delta_cdf_loader.DeltaCDFLoader.read_data">read_data</h4>

```python
def read_data(options: dict[str, str] | None = None) -> DataFrame
```

Reads data using the CDF strategy.

**Arguments**:

  options(dict[str, str], optional): Additional DataFrameReader
  options.

<h1 id="delta_loader.strategies">delta_loader.strategies</h1>

<h1 id="delta_loader.strategies.delta_timestamp_loader">delta_loader.strategies.delta_timestamp_loader</h1>

<h2 id="delta_loader.strategies.delta_timestamp_loader.DeltaTimestampConfig">DeltaTimestampConfig</h2>

```python
class DeltaTimestampConfig(BaseModel)
```

This class holds the config for the DeltaTimestampLoader.

**Arguments**:

- `timestamp_filter_cols` _list[str | Column]_ - A list of columns used for
  timestamp filtering.
- `from_timestamp` _datetime | None_ - The starting timestamp. If None, it
  starts from the beginning.
- `to_timestamp` _datetime | None_ - The ending timestamp. If None, it goes
  up to the latest timestamp.
- `filter_method` _str | None_ - The method used for filtering when multiple
  timestamp columns are used. Allowed values are '||', '&&', 'OR',
  'AND'. Defaults to None.

<h4 id="delta_loader.strategies.delta_timestamp_loader.DeltaTimestampConfig.parse_datetime">parse_datetime</h4>

```python
@field_validator("from_timestamp", "to_timestamp", mode="before")
@classmethod
def parse_datetime(cls, value)
```

Parses datetime input.

If a string is parsed, it is expected to be in ISO 8601 format.

<h4 id="delta_loader.strategies.delta_timestamp_loader.DeltaTimestampConfig.parse_filter_method">parse_filter_method</h4>

```python
@field_validator("filter_method", mode="before")
@classmethod
def parse_filter_method(cls, value)
```

Parses and validates filter_method input.

<h4 id="delta_loader.strategies.delta_timestamp_loader.DeltaTimestampConfig.check_filter_method">check_filter_method</h4>

```python
@model_validator(mode="after")
def check_filter_method()
```

Validates that a filter method is set, when more than one timestamp col is used.

<h2 id="delta_loader.strategies.delta_timestamp_loader.DeltaTimestampLoader">DeltaTimestampLoader</h2>

```python
class DeltaTimestampLoader(DeltaLoader)
```

Implementation of the DeltaLoader interface using timestamp strategy.

**Arguments**:

- `config` _DeltaTimestampConfig_ - Configuration for the
  DeltaTimestampLoader.
- `table_identifier` _str_ - Identifier for the table to be loaded.
- `delta_load_identifier` _str_ - Identifier for the delta load.
- `metadata_table_identifier` _str | None, optional_ - Identifier for the
  metadata table. Defaults to None.

<h4 id="delta_loader.strategies.delta_timestamp_loader.DeltaTimestampLoader.verify">verify</h4>

```python
def verify() -> None
```

Verify that the source table has the Change Data Feed enabled.

<h4 id="delta_loader.strategies.delta_timestamp_loader.DeltaTimestampLoader.read_data">read_data</h4>

```python
def read_data(options: dict[str, str] | None = None) -> DataFrame
```

Reads data using the Timestamp strategy.

**Arguments**:

  options(dict[str, str], optional): Additional DataFrameReader
  options.

