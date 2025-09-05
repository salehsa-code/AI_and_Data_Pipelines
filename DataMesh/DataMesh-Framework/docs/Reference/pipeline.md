# Table of Contents

* [pipeline\_parsing\_service](#pipeline_parsing_service)
* [pipeline](#pipeline)
* [actions](#actions)
* [actions.validate\_table\_columns](#actions.validate_table_columns)
* [actions.transform\_union](#actions.transform_union)
* [actions.transform\_add\_column](#actions.transform_add_column)
* [actions.create\_table](#actions.create_table)
* [actions.read\_delta\_table](#actions.read_delta_table)
* [actions.run\_notebook\_action](#actions.run_notebook_action)
* [actions.read\_files\_stream](#actions.read_files_stream)
* [actions.transform\_generic\_sql](#actions.transform_generic_sql)
* [actions.transform\_zip\_extract](#actions.transform_zip_extract)
* [actions.transform\_select\_columns](#actions.transform_select_columns)
* [actions.write\_delta\_table](#actions.write_delta_table)
* [actions.transform\_deduplication](#actions.transform_deduplication)
* [actions.transform\_replace\_values](#actions.transform_replace_values)
* [actions.create\_schema](#actions.create_schema)
* [actions.transform\_filter](#actions.transform_filter)
* [actions.list\_files](#actions.list_files)
* [actions.transform\_join](#actions.transform_join)
* [actions.execute\_sql](#actions.execute_sql)
* [actions.transform\_change\_datatype](#actions.transform_change_datatype)
* [actions.create\_volume](#actions.create_volume)
* [actions.read\_table\_metadata](#actions.read_table_metadata)
* [actions.write\_delta\_merge\_scd2](#actions.write_delta_merge_scd2)
* [actions.move\_file](#actions.move_file)
* [actions.transform\_distinct](#actions.transform_distinct)
* [actions.read\_excel](#actions.read_excel)
* [actions.write\_delta\_table\_stream](#actions.write_delta_table_stream)
* [actions.transform\_concat\_columns](#actions.transform_concat_columns)
* [actions.consume\_delta\_load](#actions.consume_delta_load)
* [actions.transform\_rename\_columns](#actions.transform_rename_columns)
* [actions.write\_file](#actions.write_file)
* [actions.read\_table\_metadata\_from\_uc](#actions.read_table_metadata_from_uc)
* [actions.transform\_convert\_timestamp](#actions.transform_convert_timestamp)
* [actions.read\_files](#actions.read_files)
* [actions.read\_data\_contract](#actions.read_data_contract)
* [actions.transform\_expand\_columns](#actions.transform_expand_columns)
* [actions.transform\_decode](#actions.transform_decode)
* [actions.read\_api](#actions.read_api)

<h1 id="pipeline_parsing_service">pipeline_parsing_service</h1>

<h2 id="pipeline_parsing_service.PipelineBaseModel">PipelineBaseModel</h2>

```python
class PipelineBaseModel(BaseModel)
```

The base model for Pipeline Config objects.

<h4 id="pipeline_parsing_service.PipelineBaseModel.metadata_to_instance">metadata_to_instance</h4>

```python
@classmethod
def metadata_to_instance(cls, data: dict)
```

Parses a Dictionary to an instance.

**Returns**:

  An instance and potentially a list of errors.

<h4 id="pipeline_parsing_service.PipelineBaseModel.handle_validation_errors">handle_validation_errors</h4>

```python
@staticmethod
def handle_validation_errors(errors: list[ValidationError]) -> None
```

Cleanly prints Pydantic validation errors and raises a ValueError.

**Arguments**:

- `errors` _list_ - A list of Pydantic validation errors.
  

**Raises**:

- `ValueError` - If any validation errors occurred.

<h2 id="pipeline_parsing_service.PipelineActionConfig">PipelineActionConfig</h2>

```python
class PipelineActionConfig(PipelineBaseModel)
```

The configuration for a Pipeline Action.

<h4 id="pipeline_parsing_service.PipelineActionConfig.validate_action">validate_action</h4>

```python
@model_validator(mode="before")
@classmethod
def validate_action(cls, v)
```

The Pipeline Action must be a valid action type.

<h2 id="pipeline_parsing_service.PipelineStepConfig">PipelineStepConfig</h2>

```python
class PipelineStepConfig(PipelineBaseModel)
```

The configuration for a Pipeline Step.

<h2 id="pipeline_parsing_service.PipelineConfig">PipelineConfig</h2>

```python
class PipelineConfig(PipelineBaseModel)
```

The configuration for a Pipeline.

<h2 id="pipeline_parsing_service.PipelineParsingService">PipelineParsingService</h2>

```python
class PipelineParsingService()
```

Reads Pipeline definition from a given Path and returns a Pipeline object.

<h4 id="pipeline_parsing_service.PipelineParsingService.register_pipeline_action">register_pipeline_action</h4>

```python
@staticmethod
def register_pipeline_action(pipeline_action_class)
```

Registers a custom pipeline action class.

!!! note
    Registering an action enables the custom action to be used in the
    pipeline YAML definition. This is automatically called, when the
    PipelineParsingService is instantiated with (a list of) custom
    actions.

<h4 id="pipeline_parsing_service.PipelineParsingService.parse_yaml">parse_yaml</h4>

```python
@staticmethod
def parse_yaml(path: Path | None = None, yaml_str: str | None = None)
```

Reads the YAML from a given Path and returns a Pipeline object.

**Arguments**:

- `path` _Path_ - Path to the YAML document.
- `yaml_str` _str_ - A string that can be parsed in YAML format.
  

**Raises**:

- `ValueError` - If neither 'path' nor 'yaml_str' has been provided.
  

**Returns**:

- `Pipeline` - The resulting Pipeline instance.

<h1 id="pipeline">pipeline</h1>

<h2 id="pipeline.PipelineContext">PipelineContext</h2>

```python
@dataclass
class PipelineContext()
```

A data class that holds the current context of a pipeline.

The context consists of Metadata (the Table definition) and the actual data
as a DataFrame.

**Attributes**:

- `metadata` _Table_ - The WinDEF-Table definition.
- `data` _DataFrame_ - The data of the context.
- `runtime_info` _dict[str, Any]_ - Additional runtime information.
- `status` _str_ - The status of the context. Can be "initialized",
  "successful" or "failed". Defaults to "initialized".

<h4 id="pipeline.PipelineContext.from_existing">from_existing</h4>

```python
def from_existing(metadata: Table | None = None,
                  data: DataFrame | None = None,
                  runtime_info: dict[str, Any] | None = None)
```

Creates a new PipelineContext from an existing one.

**Arguments**:

- `metadata` _Table, optional_ - The metadata of the new context. Defaults to None.
- `data` _DataFrame, optional_ - The data of the new context. Defaults to None.
- `runtime_info` _dict, optional_ - The runtime_info of the new context. Defaults to None.
  

**Returns**:

- `PipelineContext` - The new PipelineContext.

<h4 id="pipeline.PipelineContext.merge_runtime_info">merge_runtime_info</h4>

```python
def merge_runtime_info(new_info: dict[str, Any] | None) -> None
```

Merges the runtime_info of the context with new information.

Recursively merges the runtime_info of the context with the new
information. Lists are extended, dicts are recursively merged and
literals are overwritten from right to left.

**Arguments**:

- `new_info` _dict[str, Any], optional_ - The new information to merge.

<h2 id="pipeline.PipelineActionMeta">PipelineActionMeta</h2>

```python
class PipelineActionMeta(ABCMeta)
```

Metaclass for PipelineAction to ensure that all subclasses have a 'name' attribute.

<h2 id="pipeline.PipelineAction">PipelineAction</h2>

```python
class PipelineAction(ABC, metaclass=PipelineActionMeta)
```

Models the operation being executed against an Input.

<h4 id="pipeline.PipelineAction.run">run</h4>

```python
@abstractmethod
def run(context: PipelineContext, **kwargs: Any) -> PipelineContext
```

Execute the pipeline action.

<h2 id="pipeline.PipelineStep">PipelineStep</h2>

```python
@dataclass
class PipelineStep()
```

A PipelineStep is a logical step within a Pipeline.

The step stores the PipelineContext and offers an interface to interact with
the Steps DataFrame.

<h4 id="pipeline.PipelineStep.df">df</h4>

```python
@property
def df() -> DataFrame | None
```

The Dataframe of the Steps result.

<h4 id="pipeline.PipelineStep.run">run</h4>

```python
def run() -> None
```

Execute the action on the context.

<h2 id="pipeline.Pipeline">Pipeline</h2>

```python
class Pipeline()
```

A Pipeline represents the logical unit of one ETL process.

<h4 id="pipeline.Pipeline.add">add</h4>

```python
def add(step: PipelineStep)
```

Adds a PipelineStep to the Pipeline to be executed during run.

**Arguments**:

- `step` _PipelineStep_ - The PipelineStep to be added.
  

**Raises**:

- `ValueError` - When the Step ID has already been assigned.
  

**Returns**:

  None

<h4 id="pipeline.Pipeline.add_list">add_list</h4>

```python
def add_list(step_list: list[PipelineStep])
```

Adds a List of PipelineSteps to the Pipeline to be executed during the run.

**Arguments**:

- `step_list` _list[PipelineStep]_ - List of PipelineSteps to be added.

<h4 id="pipeline.Pipeline.run">run</h4>

```python
def run()
```

Runs the Steps added to the Pipeline in correct order.

<h4 id="pipeline.Pipeline.sort_steps">sort_steps</h4>

```python
def sort_steps() -> None
```

Sorts the steps in topological order.

This method first creates a dictionary to store the steps and their predecessors.
Then it initializes a deque and a dictionary to keep track of the visited steps.
It finally performs a topological sort on the steps and updates the execution order.

<h4 id="pipeline.Pipeline.to_mermaid">to_mermaid</h4>

```python
def to_mermaid() -> str
```

Converts the Pipeline to a mermaid diagram string.

This function is intended to be used for debugging or documentation purposes.

<h1 id="actions">actions</h1>

<h4 id="actions.PipelineActionType">PipelineActionType</h4>

type: ignore

<h1 id="actions.validate_table_columns">actions.validate_table_columns</h1>

<h2 id="actions.validate_table_columns.ValidateTableColumnsAction">ValidateTableColumnsAction</h2>

```python
class ValidateTableColumnsAction(PipelineAction)
```

This Class implements a validation action for all columns in a table.

The ValidateTableColumnsAction creates a DataValidationRunner instance and
runs all validations defined in the dataset metadata for each column.

<h4 id="actions.validate_table_columns.ValidateTableColumnsAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        raise_on_criticality: str = "error",
        exclude_warnings: bool = False,
        target_table: str | None = None,
        quarantine_invalid_data: bool = True,
        quarantine_catalog: str | None = None,
        quarantine_schema_name: str | None = None,
        quarantine_header_table_name: str | None = None,
        quarantine_records_table_name: str | None = None,
        validation_rules: list[dict[str, Any]] | None = None,
        **_: Any) -> PipelineContext
```

Run validations for each column.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `raise_on_criticality` _str_ - The level of violation that must
  fail, before the runner raises a ValidationException. Defaults
  to 'error'. Accepts 'error' and 'warning'.
- `target_table` _str_ - The target table to validate. Defaults to the
  table from the metadata and None if not found.
- `quarantine_invalid_data` _bool_ - Decides if the quarantine mechanism
  is run. Defaults to True.
- `quarantine_catalog` _str_ - Name of the catalog where the quarantine
  tables are stored.
- `quarantine_schema_name` _str, optional_ - Name of the quarantine
  schema. Defaults to 'quarantine' or
  `WINDEF__Q_QUARANTINE_HEADER_TABLE` environment variable.
- `quarantine_header_table_name` _str_ - Name of the Quarantine Header
  table. Defaults to 'quarantine_header' or
  `WINDEF__Q_QUARANTINE_HEADER_TABLE` environment variable.
- `quarantine_records_table_name` _str_ - Name of the Quarantine Records
  table. Defaults to 'quarantine_records' or
  `WINDEF__Q_QUARANTINE_RECORDS_TABLE` environment variable.
- `validation_rules` _list[dict[str, Any]]_ - List of validation rules
  to be applied to the data. Defaults to None. Extends the validation
  rules defined in the metadata.
- `exclude_warnings` _bool_ - Decides if warnings should be excluded from
  the result. Defaults to False.
  

**Raises**:

- `ValueError` - If no columns are defined in the metadata.
- `ValidationError` - If invalid quarantine configurations are passed.
- `ValueError` - If the raise_on_criticality is not 'error' or 'warning'.
  

**Returns**:

- `PipelineContext` - The context with the validated data.

<h1 id="actions.transform_union">actions.transform_union</h1>

<h2 id="actions.transform_union.TransformUnionAction">TransformUnionAction</h2>

```python
class TransformUnionAction(PipelineAction)
```

A transformer step to union DataFrames together.

<h4 id="actions.transform_union.TransformUnionAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        union_data: list[PipelineStep] | None = None,
        **_: Any) -> PipelineContext
```

A transformer step to union DataFrames together.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `union_data` _list[PipelineStep]_ - The PipelineSteps context defines the DataFrame
  to union with current context.
  

**Raises**:

- `ValueError` - If no union_data is provided.
- `ValueError` - If the data from context is None.
- `ValueError` - If the data from any of the union_data is None.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.transform_add_column">actions.transform_add_column</h1>

<h2 id="actions.transform_add_column.TransformAddColumnAction">TransformAddColumnAction</h2>

```python
class TransformAddColumnAction(PipelineAction)
```

This class implements a Transform action for an ETL pipeline.

The TransformAddColumnAction adds a column to the DataFrame.

<h4 id="actions.transform_add_column.TransformAddColumnAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        columns: dict[str, Any] | None = None,
        **_: Any) -> PipelineContext
```

Adds a column to the DataFrame.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `columns` _dict[str, Any]_ - A dictionary where the key is a column
  name and the value is the value the column will be initialized with.
  

**Raises**:

- `ValueError` - If no columns are provided.
- `ValueError` - If the data from context is None.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.create_table">actions.create_table</h1>

<h2 id="actions.create_table.CreateDeltaTableAction">CreateDeltaTableAction</h2>

```python
class CreateDeltaTableAction(PipelineAction)
```

This class implements an action to create a delta table.

**Returns**:

  PipelineContext

<h4 id="actions.create_table.CreateDeltaTableAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        ignore_if_exists: bool = True,
        properties: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
        **_: Any) -> PipelineContext
```

An Action to create a delta table.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `ignore_if_exists` _bool, optional_ - Ignore table creation if table
  already exists. Defaults to True.
- `properties` _dict, optional_ - The properties of the table. Defautls to None.
- `options` _dict, optional_ - The options for the table. Defautls to None.
  

**Returns**:

  None

<h1 id="actions.read_delta_table">actions.read_delta_table</h1>

<h2 id="actions.read_delta_table.ReadTableAction">ReadTableAction</h2>

```python
class ReadTableAction(PipelineAction)
```

This class implements a Read action for an ETL pipeline.

The ReadFilesAction reads data from a source, defined by input variables and
returns a DataFrame.

<h4 id="actions.read_delta_table.ReadTableAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        table_name: str | None = None,
        options: dict[str, str] | None = None,
        delta_load_options: dict[str, str] | None = None,
        **_: Any) -> PipelineContext
```

Reads a Delta table from unity catalog.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `table_name` _str, optional_ - The name of the Delta table to read. If
  not set, the table specified in the metadata context will be read.
  Defaults to None.
- `options` _dict[str, str], optional_ - Additional options passed to the
  reader. Defaults to None.
- `delta_load_options` _dict[str, str], optional_ - Options for delta loads.
  Defaults to None.
  

**Raises**:

- `ValueError` - Raised when neither table_name nor valid metadata is
  specified.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.run_notebook_action">actions.run_notebook_action</h1>

<h2 id="actions.run_notebook_action.RunNotebookAction">RunNotebookAction</h2>

```python
class RunNotebookAction(PipelineAction)
```

A transformer step to run ETLs defined in another notebook.

<h4 id="actions.run_notebook_action.RunNotebookAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        notebook_path: str | None = None,
        timeout_seconds: int = 0,
        **kwargs) -> PipelineContext
```

Run another notebook passing the DataFrame back and forth as a temp view.

A temporary view is created from the current DataFrame. The ETL notebook
is run with the name of the temporary view as input. A new DataFrame is
read from a temporary view created in the external notebook.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `notebook_path` _str_ - Path to the ETL notebook. This notebook must be
  accessible from the workspace where the ETL pipeline is executed.
- `timeout_seconds` _int_ - Timeout of the run. An error is raised by
  Databricks if the run doesn't finish within the specified time in
  seconds. A timeout value of 0 means, no timeout. Defaults to 0.
- `**kwargs` - Additional keyword arguments are passed as arguments to
  the notebook.
  

**Raises**:

- `ValueError` - Raised if no notebook path is provided.
- `ValueError` - Raised if the data from context is None.
- `TypeError` - Raised if notebook parameters are of invalid types.

<h1 id="actions.read_files_stream">actions.read_files_stream</h1>

<h2 id="actions.read_files_stream.ReadFilesStreamAction">ReadFilesStreamAction</h2>

```python
class ReadFilesStreamAction(PipelineAction)
```

This class implements a Read action for an ETL pipeline.

The ReadFilesStreamAction streams data from a source, defined by input variables
and returns a DataFrame.

<h4 id="actions.read_files_stream.ReadFilesStreamAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        path: str = "",
        source_format: str | None = None,
        schema: str | None = None,
        include_source_file_column: bool = True,
        options: dict[str, str] | None = None,
        **_: Any) -> PipelineContext
```

Streams files from a path.

When given an extension, all files with the given extension will be
read. Otherwise the source_format must be set, then all files in the
path will be read using a DataFrameReader with the given format.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `path` _str_ - The path to read files from.
- `extension` _str, optional_ - Extension of files to be included.
  Defaults to None.
- `source_format` _str, optional_ - Format of the DataFrameReader.
  Defaults to None.
- `schema` _str, optional_ - Schema of the data. If None,
  schema is read from context metadata.
- `include_source_file_column` _bool_ - Decides if the column
  `_source_file` is included, containing the file, where the data
  was read from. Defaults to False.
- `options` _dict[str, str], optional_ - Additional options passed to the
  reader. Defaults to None.
  

**Raises**:

- `ValueError` - Raised when neither extension nor source_format are
  defined.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.transform_generic_sql">actions.transform_generic_sql</h1>

<h2 id="actions.transform_generic_sql.TransformSqlAction">TransformSqlAction</h2>

```python
class TransformSqlAction(PipelineAction)
```

A transformer step to execute generic SQL statements.

<h4 id="actions.transform_generic_sql.TransformSqlAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        sql_statement: str = "",
        **kwargs) -> PipelineContext
```

Execute a SQL statement on a dataframe.

A temporary view is created from the current dataframe. The SQL statement
is executed on that view and stored as new dataframe.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `sql_statement` _str_ - A string containing the SQL statement to be
  executed. The source table should be referred to as "df".
- `**kwargs` - Additional keyword arguments are passed as kwargs to the
  pyspark sql method to replace placeholders in the query.
  

**Raises**:

- `ValueError` - Raised if "{DATA_FRAME}" is not used as reference to the
  source table in the sql_statement.
- `ValueError` - Raised if no SQL statement is provided.
- `ValueError` - Raised if the data from context is None.

<h1 id="actions.transform_zip_extract">actions.transform_zip_extract</h1>

<h2 id="actions.transform_zip_extract.TransformZipExtractAction">TransformZipExtractAction</h2>

```python
class TransformZipExtractAction(PipelineAction)
```

This class implements a Transform action for an ETL pipeline.

The TransformZipExtractAction interprets a byte string in a given column as
a zip file and extracts it. The content of the zip file is added two
columns, `file_name` and `file_content`. The DataFrame is exploded so that one
row per file within the zip file is produced.

<h4 id="actions.transform_zip_extract.TransformZipExtractAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        column: str | None = None,
        name_prefix: str | None = None,
        **_: Any) -> PipelineContext
```

Extracts the content of the column.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `column` _str_ - Column name containing the zip file byte string.
- `name_prefix` _str, optional_ - A prefix for the `file_name` and
  `file_content` columns.
  

**Raises**:

- `ValueError` - If no column is specified.
- `ValueError` - If no columns are provided.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.transform_select_columns">actions.transform_select_columns</h1>

<h2 id="actions.transform_select_columns.TransformSelectColumnsAction">TransformSelectColumnsAction</h2>

```python
class TransformSelectColumnsAction(PipelineAction)
```

This class implements a Transform action for an ETL pipeline.

The TransformSelectColumnsAction selects the given columns from a DataFrame
and returns a new DataFrame consisting of the selected columns.

<h4 id="actions.transform_select_columns.TransformSelectColumnsAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        include_columns: list[str] | None = None,
        exclude_columns: list[str] | None = None,
        **_: Any) -> PipelineContext
```

Renames the columns for the given DataFrame.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `include_columns` _list[str]_ - A list of column names that should be included. Defaults to None.
- `exclude_columns` _list[str]_ - A list of column names that should be excluded. Defaults to None.
  

**Raises**:

- `ValueError` - If a column is specified that is not in the DataFrame.
- `ValueError` - If no columns are provided.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.write_delta_table">actions.write_delta_table</h1>

<h2 id="actions.write_delta_table.AppendToDeltaAction">AppendToDeltaAction</h2>

```python
class AppendToDeltaAction(PipelineAction)
```

This class implements a Write action for an ETL pipeline.

The WriteFileAction write a Dataframe to a storage location defined in the
options.

**Returns**:

  None.

<h4 id="actions.write_delta_table.AppendToDeltaAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        ignore_empty_df: bool = False,
        create_if_not_exists: bool = True,
        refresh_table: bool = True,
        create_view: bool = False,
        options: dict[str, str] | None = None,
        table_identifier: str | None = None,
        **_: Any) -> PipelineContext
```

Append the DataFrame to the delta table.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `ignore_empty_df` _bool, optional_ - A flag indicating whether to
  ignore an empty source DataFrame. Defaults to False.
- `create_if_not_exists` _bool, optional_ - Create the table if it not
  exists. Defaults to True.
- `refresh_table` _bool, optional_ - Refresh the table after the
  transaction. Defaults to True.
- `create_view` _bool, optional_ - Automatically create a default view
  for the table. Defaults to False.
- `options` _dict_ - Additional DataFrame writer options. Default None.
- `table_identifier` _str, optional_ - The identifier of the table. If passed, the
  UC Adapter will be used to create a table object. Defaults to None.
  

**Raises**:

- `ValueError` - If the table does not exist.
- `ValueError` - If the table metadata is empty.
- `ValueError` - If the table could not be found.
  

**Returns**:

  Pipeline Context

<h2 id="actions.write_delta_table.MergeIntoDeltaAction">MergeIntoDeltaAction</h2>

```python
class MergeIntoDeltaAction(PipelineAction)
```

This class implements a Write action for an ETL pipeline.

The WriteFileAction write a Dataframe to a storage location defined in the
options.

**Returns**:

  None.

<h4 id="actions.write_delta_table.MergeIntoDeltaAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        table_identifier: str | None = None,
        key_columns: list[str] | None = None,
        cols_to_update: list[str] | None = None,
        cols_to_insert: list[str] | None = None,
        cols_to_exclude: list[str] | None = None,
        when_matched_update: bool = True,
        when_matched_deleted: bool = False,
        when_not_matched_insert: bool = True,
        use_partition_pruning: bool = True,
        ignore_empty_df: bool = False,
        create_if_not_exists: bool = True,
        refresh_table: bool = True,
        create_view: bool = False,
        **_: Any) -> PipelineContext
```

Merge the dataframe into the delta table.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `table_identifier` _str, optional_ - The identifier of the table. If passed, the
  UC Adapter will be used to create a table object. Defaults to None.
- `key_columns` _List[str], optinal_ - List of column names that form the
  key for the merge operation. Defaults to the primary key of the
  table.
- `when_matched_update` _bool, optional_ - Flag to specify whether to
  perform an update operation whenmatching records are found in
  the target Delta table. Defaults to True.
- `when_matched_deleted` _bool, optional_ - Flag to specify whether to
  perform a delete operation when matching records are found in
  the target Delta table. Defaults to False.
- `when_not_matched_insert` _bool, optional_ - Flag to specify whether to
  perform an insert operation when matching records are not found
  in the target Delta table. Defaults to True.
- `cols_to_update` _List[str], optional_ - List of column names to be
  updated in the target Delta table. Defaults to columns of df.
- `cols_to_insert` _List[str], optional_ - List of column names to be
  inserted into the target Delta table. Defaults to columns of df.
- `cols_to_exclude` _List[str], optional_ - List of column names to be
  excluded from the merge operation. Defaults to None.
- `use_partition_pruning` _bool, optional_ - Flag to specify whether to
  use partition pruning to optimize the performance of the merge
  operation. Defaults to True.
- `ignore_empty_df` _bool, optional_ - A flag indicating whether to
  ignore an empty source dataframe. Defaults to False.
- `create_if_not_exists` _bool, optional_ - Create the table if it not
  exists. Defaults to True.
- `refresh_table` _bool, optional_ - Refresh the table after the
  transaction. Defaults to True.
- `create_view` _bool, optional_ - Automatically create a default view
  for the table. Defaults to False.
  

**Raises**:

- `ValueError` - If the table does not exist.
- `ValueError` - If the data is not set in the pipeline context.
- `ValueError` - If the table metadata is empty.
  

**Returns**:

  Pipeline Context

<h1 id="actions.transform_deduplication">actions.transform_deduplication</h1>

<h2 id="actions.transform_deduplication.TransformDeduplicationAction">TransformDeduplicationAction</h2>

```python
class TransformDeduplicationAction(PipelineAction)
```

Deduplicates the data from the given DataFrame.

This method deduplicates the data where the key columns are the same
and keeps the entry with the highest values in the order_by_columns
(can be changed to lowest by setting the parameter descending to false).

**Example**:

```yaml
Deduplicate Columns:
    action: TRANSFORM_DEDUPLICATION
    options:
        key_columns:
            - id
        order_by_columns:
            - source_file_modification_time
```

<h4 id="actions.transform_deduplication.TransformDeduplicationAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        key_columns: list[str] | None = None,
        order_by_columns: list[str] | None = None,
        descending: bool = True,
        **_: Any) -> PipelineContext
```

Deduplicates the data based on key columns and order by columns.

**Arguments**:

- `context` - The context in which this Action is executed.
- `key_columns` - A list of the key column names. The returned data only keeps one
  line of data with the same key columns.
- `order_by_columns` - A list of order by column names. The returned data keeps the
  first line of data with the same key columns ordered by these columns.
- `descending` - Whether to sort descending or ascending.
  

**Raises**:

- `ValueError` - If no key_columns are specified.
- `ValueError` - If no order_by_columns are specified.
- `ValueError` - If the data from context is None.
- `ValueError` - If key_columns and order_by_columns overlap.
- `ValueError` - If key_columns or order_by_columns contain Nulls.
  

**Returns**:

  The context after the execution of this Action, containing the DataFrame with the deduplicated data.

<h1 id="actions.transform_replace_values">actions.transform_replace_values</h1>

<h2 id="actions.transform_replace_values.TransformReplaceValuesAction">TransformReplaceValuesAction</h2>

```python
class TransformReplaceValuesAction(PipelineAction)
```

This class implements a Transform action for an ETL pipeline.

The TransformReplaceValuesAction replaces specified values in columns of a DataFrame.

<h4 id="actions.transform_replace_values.TransformReplaceValuesAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        replace: dict[str, dict[str, str]] | None = None,
        **_: Any) -> PipelineContext
```

Replaces specified values in columns of a DataFrame.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `replace` _dict[str, str]_ - A dictionary defining the columns and
  replaced values. The key is the column name and the value is a
  dictionary with old_value -> new_value as key-value pairs.
  

**Raises**:

- `ValueError` - If no replace values are provided.
- `ValueError` - If the data from context is None.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.create_schema">actions.create_schema</h1>

<h2 id="actions.create_schema.CreateSchemaAction">CreateSchemaAction</h2>

```python
class CreateSchemaAction(PipelineAction)
```

This class implements an action to create a schema.

**Returns**:

  PipelineContext

<h4 id="actions.create_schema.CreateSchemaAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        catalog: str | None = None,
        schema: str | None = None,
        location: str | None = None,
        comment: str | None = None,
        options: dict[str, Any] | None = None,
        **_: Any) -> PipelineContext
```

An Action to create a delta schema.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `catalog` _str_ - The catalog in which the schema will be created.
- `schema` _str_ - The name of the schema.
- `location` _str_ - The managed location for the schema.
- `comment` _str_ - A comment for the schema.
- `options` _dict[str, Any], optional_ - Additional options for schema creation.
  Defaults to None.
  

**Raises**:

- `ValueError` - If 'catalog', 'schema', or 'location' are not provided.
  

**Returns**:

  PipelineContext

<h1 id="actions.transform_filter">actions.transform_filter</h1>

<h2 id="actions.transform_filter.TransformFilterAction">TransformFilterAction</h2>

```python
class TransformFilterAction(PipelineAction)
```

This class implements a Transform action for an ETL pipeline.

The TransformFilterAction filters a dataframe based on a SQL-like where
statement.

<h4 id="actions.transform_filter.TransformFilterAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        condition: str = "",
        **_: Any) -> PipelineContext
```

Renames the columns for the given DataFrame.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `condition` _str_ - A SQL expression used to filter the dataframe.
  

**Raises**:

- `ValueError` - If no condition is provided.
- `ValueError` - If the data from context is None.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.list_files">actions.list_files</h1>

<h2 id="actions.list_files.ListFilesAction">ListFilesAction</h2>

```python
class ListFilesAction(PipelineAction)
```

This class implements a List action for an ETL pipeline.

The ListFilesAction lists files in a directory and returns the file paths in
the contexts runtime_info under the key 'read_files'. This allows to further
process the files in the pipeline, e.g. in the MOVE_FILES action.

<h4 id="actions.list_files.ListFilesAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        location: str | None = None,
        file_name_pattern: str | None = None,
        runtime_info_key: str = "read_files",
        search_subdirs: bool = True,
        create_dataframe: bool = False,
        **_: Any) -> PipelineContext
```

List files in a directory and return them as part of the runtime_info.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `location` _str_ - The location to search for files. This could be a path to a local directory or a URI for blob storage.
- `file_name_pattern` _str_ - The file file_name_pattern to filter by as a regex pattern. None retrieves all files regardless of file_name_pattern.
- `runtime_info_key` _str_ - The key in runtime_info to store the file paths under.
- `search_subdirs` _bool_ - Whether to include files from subdirectories in the search.
- `create_dataframe` _bool_ - Whether to create a DataFrame with the file paths.

<h1 id="actions.transform_join">actions.transform_join</h1>

<h2 id="actions.transform_join.TransformJoinAction">TransformJoinAction</h2>

```python
class TransformJoinAction(PipelineAction)
```

A transformer step to join two DataFrames together.

<h4 id="actions.transform_join.TransformJoinAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        joined_data: PipelineStep | None = None,
        join_on: list[str] | str | dict[str, str] | None = None,
        how: str = "inner",
        **_: Any) -> PipelineContext
```

A transformer step to join two DataFrames together.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `joined_data` _PipelineStep_ - The PipelineSteps context defines the DataFrame
  to join with as right side of the join.
- `join_on` _list[str]|str|dict[str,str]_ - A string for the join column
  name, a list of column names, a join expression (Column), or a
  list of Columns. If on is a string or a list of strings
  indicating the name of the join column(s), the column(s) must
  exist on both sides, and this performs an equi-join. If a
  dictionary is used, the key is used as the column name in the
  'left' table and the value is the column name in the 'right'
  table.
- `how` _str_ - Must be one of: inner, cross, outer, full,
  fullouter, full_outer, left, leftouter, left_outer, right,
  rightouter, right_outer, semi, leftsemi, left_semi, anti, leftanti
  and left_anti. Defaults to inner.
  

**Raises**:

- `ValueError` - If no joined_data is provided.
- `ValueError` - If no join_on is provided.
- `ValueError` - If the data from context is None.
- `ValueError` - If the data from the joined_data is None.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.execute_sql">actions.execute_sql</h1>

<h2 id="actions.execute_sql.ExecuteSqlAction">ExecuteSqlAction</h2>

```python
class ExecuteSqlAction(PipelineAction)
```

An action to execute generic SQL statements.

These statements do NOT alter the data in the context. They can be used to
execute arbitrary SQL, e.g. to create views or alter permissions.

<h4 id="actions.execute_sql.ExecuteSqlAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        sql_statement: str | None = None,
        file_path: str | None = None,
        variables: dict[str, str] | None = None,
        **_: Any) -> PipelineContext
```

Execute a SQL statement.

The statement does NOT alter the data in context. If that is what is
required, please use the TRANSFORM_SQL action.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `sql_statement` _str_ - A string containing the SQL statement to be
  executed.
- `file_path` _str_ - Path to a SQL file containing the SQL statement to
  be executed.
- `variables` _dict[str, str]_ - A dictionary of variables to be replaced
  in the SQL file.
  

**Raises**:

- `ValueError` - If both sql_statement and file_path are specified.
- `ValueError` - If neither sql_statement nor file_path are specified.
  

**Returns**:

- `PipelineContext` - The context in which this Action was executed.

<h1 id="actions.transform_change_datatype">actions.transform_change_datatype</h1>

<h2 id="actions.transform_change_datatype.TransformChangeDatatypeAction">TransformChangeDatatypeAction</h2>

```python
class TransformChangeDatatypeAction(PipelineAction)
```

This class implements a Transform action for an ETL pipeline.

The TransformChangeDatatypeAction changes the datatypes of columns in a DataFrame.

<h4 id="actions.transform_change_datatype.TransformChangeDatatypeAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        columns: dict[str, str] | None = None,
        **_: Any) -> PipelineContext
```

Changes datatypes of columns for the given DataFrame.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `columns` _dict[str, str]_ - A dictionary where the key is a column
  name and the value is the desired datatype.
  

**Raises**:

- `ValueError` - If no columns are provided.
- `ValueError` - If the data from context is None.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.create_volume">actions.create_volume</h1>

<h2 id="actions.create_volume.CreateVolumeAction">CreateVolumeAction</h2>

```python
class CreateVolumeAction(PipelineAction)
```

This class implements an action to create a volume.

**Returns**:

  PipelineContext

<h4 id="actions.create_volume.CreateVolumeAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        volume_name: str | None = None,
        location: str | None = None,
        ignore_if_exists: bool = True,
        comment: str = "This volume was created by the CREATE_VOLUME action.",
        **_: Any) -> PipelineContext
```

An Action to create a volume.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `volume_name` _str, optional_ - The name of the volume. Defaults to None.
- `location` _str, optional_ - The location of the volume. Defaults to None.
- `ignore_if_exists` _bool, optional_ - Ignore volume creation if it
  already exists. Defaults to True.
- `comment` _str, optional_ - Comment to add to the volume. Defaults to
  "This volume was created by the CREATE_VOLUME action.".
  

**Raises**:

- `ValueError` - If volume location or name are not provided.
  

**Returns**:

  None

<h1 id="actions.read_table_metadata">actions.read_table_metadata</h1>

<h2 id="actions.read_table_metadata.ReadDataframeMetadataAction">ReadDataframeMetadataAction</h2>

```python
class ReadDataframeMetadataAction(PipelineAction)
```

This class implements the option to infere table metadata from a DataFrame.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `table_identifier` _str_ - Identifier of the table in the format 'catalog.schema.table'.
- `location` _str_ - Location on the physical storage.
- `primary_key` _str, optional_ - Primary key column of the table.
  Defaults to None.
- `partitioned_by` _list[str], optional_ - Partition columns of the
  table. Defaults to None.
- `use_liquid_clustering` _bool_ - Use liquid clustering. Defaults to
  true, requires Databricks Runtime 13.3 LTS or above.
  

**Raises**:

- `ValueError` - If no table identifier is provided.
- `ValueError` - If no location is provided.

<h4 id="actions.read_table_metadata.ReadDataframeMetadataAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        table_identifier: str = "",
        location: str = "",
        primary_key: str | None = None,
        partitioned_by: list[str] | None = None,
        use_liquid_clustering: bool = True,
        **_: Any) -> PipelineContext
```

Get table metadata from DataFrame using adapter.

<h1 id="actions.write_delta_merge_scd2">actions.write_delta_merge_scd2</h1>

<h2 id="actions.write_delta_merge_scd2.MergeScd2IntoDeltaAction">MergeScd2IntoDeltaAction</h2>

```python
class MergeScd2IntoDeltaAction(PipelineAction)
```

This class implements a Write action for an ETL pipeline.

The MergeScd2IntoDeltaAction merges a Dataframe to a Delta table using
Slowly Changing Dimension Type 2 (SCD2) logic.

**Returns**:

  None.

<h4 id="actions.write_delta_merge_scd2.MergeScd2IntoDeltaAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        table_identifier: str | None = None,
        key_columns: list[str] | None = None,
        cols_to_update: list[str] | None = None,
        cols_to_insert: list[str] | None = None,
        cols_to_exclude: list[str] | None = None,
        when_matched_update: bool = True,
        when_matched_deleted: bool = False,
        when_not_matched_insert: bool = True,
        use_partition_pruning: bool = True,
        ignore_empty_df: bool = False,
        create_if_not_exists: bool = True,
        refresh_table: bool = True,
        create_view: bool = False,
        current_col_name: str = "SCD_IS_CURRENT",
        start_date_col_name: str = "SCD_START_DATE",
        end_date_col_name: str = "SCD_END_DATE",
        **_: Any) -> PipelineContext
```

Merge the dataframe into the delta table.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `table_identifier` _str, optional_ - The identifier of the table. If passed, the
  UC Adapter will be used to create a table object. Defaults to None.
- `key_columns` _List[str], optinal_ - List of column names that form the
  key for the merge operation. Defaults to the primary key of the
  table.
- `when_matched_update` _bool, optional_ - Flag to specify whether to
  perform an update operation whenmatching records are found in
  the target Delta table. Defaults to True.
- `when_matched_deleted` _bool, optional_ - Flag to specify whether to
  perform a delete operation when matching records are found in
  the target Delta table. Defaults to False.
- `when_not_matched_insert` _bool, optional_ - Flag to specify whether to
  perform an insert operation when matching records are not found
  in the target Delta table. Defaults to True.
- `cols_to_update` _List[str], optional_ - List of column names to be
  updated in the target Delta table. Defaults to columns of df.
- `cols_to_insert` _List[str], optional_ - List of column names to be
  inserted into the target Delta table. Defaults to columns of df.
- `cols_to_exclude` _List[str], optional_ - List of column names to be
  excluded from the merge operation. Defaults to None.
- `use_partition_pruning` _bool, optional_ - Flag to specify whether to
  use partition pruning to optimize the performance of the merge
  operation. Defaults to True.
- `ignore_empty_df` _bool, optional_ - A flag indicating whether to
  ignore an empty source dataframe. Defaults to False.
- `create_if_not_exists` _bool, optional_ - Create the table if it not
  exists. Defaults to True.
- `refresh_table` _bool, optional_ - Refresh the table after the
  transaction. Defaults to True.
- `create_view` _bool, optional_ - Automatically create a default view
  for the table. Defaults to False.
- `current_col_name` _str, optional_ - The name of the column that
  indicates whether a record is current. Defaults to "SCD_IS_CURRENT".
- `start_date_col_name` _str, optional_ - The name of the column that
  indicates the start date of a record. Defaults to "SCD_START_DATE".
- `end_date_col_name` _str, optional_ - The name of the column that
  indicates the end date of a record. Defaults to "SCD_END_DATE".
  

**Raises**:

- `ValueError` - If the table does not exist.
- `ValueError` - If the data is not set in the pipeline context.
- `ValueError` - If the table metadata is empty.
  

**Returns**:

  Pipeline Context

<h1 id="actions.move_file">actions.move_file</h1>

<h2 id="actions.move_file.MoveFilesAction">MoveFilesAction</h2>

```python
class MoveFilesAction(PipelineAction)
```

This class implements an action to move files for an ETL pipeline.

The MoveFilesAction moves files from a source, to another location. The files
can either be explicitly specified or will take the read_files list from the
runtime_info context.

<h4 id="actions.move_file.MoveFilesAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        source_column: str | None = None,
        destination_column: str | None = None,
        files: list[str] | None = None,
        destination: str | None = None,
        base_directory: str | None = None,
        runtime_info_input_key: str = "read_files",
        runtime_info_result_key: str = "moved_files",
        ignore_file_not_found: bool = False,
        **_: Any) -> PipelineContext
```

Move files to a new destination.

If files are specified, these files will be moved, otherwise the action
will move all files stored in the runtime_info under the specified
runtime_info_input_key. The moved files will be stored in the
runtime_info under the specified runtime_info_result_key.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `files` _list[str], optional_ - The path to read files from.
- `source_column` _str_ - Column name containing the source path.
- `destination_column` _str_ - Column name containing the target path.
- `destination` _str_ - The path where the files are moved to.
- `base_directory` _str, optional_ - The base directory from which the
  files are read.
- `runtime_info_input_key` _str, optional_ - The key in runtime_info to
  get the files list from. Defaults to "read_files".
- `runtime_info_result_key` _str, optional_ - The key in runtime_info to
  store the moved files list. Defaults to "moved_files".
- `ignore_file_not_found` _bool, optional_ - Configures if missing files
  are ignored, or if an error is raised. If set to true, the action
  will just skip missing files, if false, an error will be raised.
  Defaults to False.
  

**Raises**:

- `ValueError` - Raised when no files are specified and the runtime_info
  does not contain the specified runtime_info_input_key information.
- `ValueError` - Raised when destination is not specified.
- `ValueError` - Raised when any of the specified files does not exist.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.transform_distinct">actions.transform_distinct</h1>

<h2 id="actions.transform_distinct.TransformDistinctAction">TransformDistinctAction</h2>

```python
class TransformDistinctAction(PipelineAction)
```

This class implements a Transform action for an ETL pipeline.

The TransformDistinctAction returns a Dataframe with distinct rows.

<h4 id="actions.transform_distinct.TransformDistinctAction.run">run</h4>

```python
def run(context: PipelineContext, **_: Any) -> PipelineContext
```

Selects distinct rows of the given DataFrame.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
  

**Raises**:

- `ValueError` - If the data from context is None.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.read_excel">actions.read_excel</h1>

<h2 id="actions.read_excel.ReadExcelAction">ReadExcelAction</h2>

```python
class ReadExcelAction(PipelineAction)
```

This class implements a Read action for Excel Files.

The ReadExcelAction reads data from a Excel file, defined by input variables
and returns a DataFrame.

<h4 id="actions.read_excel.ReadExcelAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        file: str | None = None,
        path: str | None = None,
        extension: str = "xlsx",
        recursive: bool = False,
        sheet_name: str | int | list = 0,
        sheet_name_as_column: bool = False,
        header: int | list[int] = 0,
        index_col: int | list[int] | None = None,
        usecols: int | str | list | Callable | None = None,
        dtype: str | None = None,
        fillna: str | dict[str, list[str]] | dict[str, str] | None = None,
        true_values: list | None = None,
        false_values: list | None = None,
        nrows: int | None = None,
        na_values: str | list[str] | dict[str, list[str]] | dict[str, str]
        | None = None,
        keep_default_na: bool = True,
        parse_dates: bool | list | dict = False,
        date_parser: Callable | None = None,
        thousands: str | None = None,
        include_index: bool = False,
        options: dict | None = None,
        **_) -> PipelineContext
```

Reads files from a path.

When given an extension, all files with the given extension will be
read. Otherwise the source_format must be set, then all files in the
path will be read using a DataFrameReader with the given format.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `file` _str_ - Location of file to read. Default None. Either path or
  file needs to be specified.
- `path` _str_ - Location of files to read. Default None. Either path or
  file needs to be specified.
- `extension` _str_ - If path is specified, decides the file extension that is
  used to identify Excel files. Defaults to "xlsx".
- `recursive` _bool_ - If path is specified, decides if subdirs
  are included in the file list. Defaults to False.
- `sheet_name` _str|int|list_ - Strings are used for sheet names.
  Integers are used in zero-indexed sheet positions. Lists of
  strings/integers are used to request multiple sheets. Specify None
  to get all sheets. Defaults to 0.
- `sheet_name_as_column` _bool_ - Add a column containing the sheet_name.
  Only works if sheet_name is specified. Defaults to False.
- `header` _header: int|list[int]_ - Row to use for column labels. If a
  list of integers is passed those row positions will be combined.
  Use None if there is no header. Defaults to 0.
- `index_col` _int|list[int]_ - Column to use as the row labels of the
  DataFrame. Pass None if there is no such column. If a list is
  passed, those columns will be combined. Defaults to None.
- `usecols` _int|str|list|Callable_ - Return a subset of the columns. If
  None, then parse all columns. If str, then indicates comma
  separated list of Excel column letters and column ranges (e.g.
  “A:E” or “A,C,E:F”). Ranges are inclusive of both sides. nIf
  list of int, then indicates list of column numbers to be parsed.
  If list of string, then indicates list of column names to be
  parsed. If Callable, then evaluate each column name against it
  and parse the column if the Callable returns True. Defaults to
  None.
- `dtype` _str|dict[str,str]_ - Data type for data or columns. Defaults to None.
- `fillna` _str|dict[str,list[str]]|dict[str, str]_ - If specified, fills
  NaN / Null values in columns using the specified fillna method.
  Defaults to None.
- `true_values` _list_ - Values to consider as True. Defaults to None.
- `false_values` _list_ - Values to consider as False. Defaults to None.
- `nrows` _int_ - Number of rows to parse. Defaults to None.
- `na_values` _list[str]|dict[str]_ - Additional strings to recognize as
  NA/NaN. If dict passed, specific per-column NA values. Defaults
  to None.
- `keep_default_na` _bool_ - If na_values are specified and
  keep_default_na is False the default NaN values are overridden,
  otherwise they're appended to. Defaults to True.
- `parse_dates` _bool, list, dict_ - The behavior is as follows:
  - bool. If True -> try parsing the index.
  - list of int or names. e.g. If [1, 2, 3] -> try parsing columns
  1, 2, 3 each as a separate date column.
  - list of lists. e.g. If [[1, 3]] -> combine columns 1 and 3 and
  parse as a single date column.
  - dict, e.g. {{"foo" : [1, 3]}} -> parse columns 1, 3 as date
  and call result "foo"
  If a column or index contains an unparseable date, the entire
  column or index will be returned unaltered as an object data
  type. Defaults to False.
- `date_parser` _function_ - Function to use for converting a sequence of
  string columns to an array of datetime instances. The default
  uses dateutil.parser.parser to do the conversion.
- `thousands` _str_ - Thousands separator for parsing string columns to
  numeric. Note that this parameter is only necessary for columns
  stored as TEXT in Excel, any numeric columns will automatically
  be parsed, regardless of display format. Defaults to None.
- `include_index` _bool_ - Include an index column. The column will be
  named `_index`.
- `options` _dict_ - Optional keyword arguments passed to
  pyspark.pandas.read_excel and handed to TextFileReader. Defaults
  to None.
  

**Raises**:

- `ValueError` - Raised when neither file nor path are
  defined. Or both are defined.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.write_delta_table_stream">actions.write_delta_table_stream</h1>

<h2 id="actions.write_delta_table_stream.AppendToDeltaStreamAction">AppendToDeltaStreamAction</h2>

```python
class AppendToDeltaStreamAction(PipelineAction)
```

This class implements a Write action for an ETL pipeline.

The AppendToDeltaStreamAction write a DataFrame to a storage location defined in the
options.

**Returns**:

  None.

<h4 id="actions.write_delta_table_stream.AppendToDeltaStreamAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        checkpoint_location: str | None = None,
        ignore_empty_df: bool = False,
        create_if_not_exists: bool = True,
        refresh_table: bool = True,
        options: dict[str, str] | None = None,
        **_: Any) -> PipelineContext
```

Append the DataFrame to the delta table.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `checkpoint_location` _str_ - Location of checkpoint. Defaults to location of table being written,
  with '_checkpoint_' added before name. Default None.
- `ignore_empty_df` _bool, optional_ - A flag indicating whether to
  ignore an empty source DataFrame. Defaults to False.
- `create_if_not_exists` _bool, optional_ - Create the table if it not
  exists. Defaults to True.
- `refresh_table` _bool, optional_ - Refresh the table after the
  transaction. Defaults to True.
- `options` _dict_ - Additional DataFrame writer options. Default None.
  

**Raises**:

- `ValueError` - If the table does not exist.
- `ValueError` - If the data is not set in the pipeline context.
- `ValueError` - If the table metadata is empty.
  RuntimeError:
  

**Returns**:

  Pipeline Context

<h1 id="actions.transform_concat_columns">actions.transform_concat_columns</h1>

<h2 id="actions.transform_concat_columns.TransformConcatColumnsAction">TransformConcatColumnsAction</h2>

```python
class TransformConcatColumnsAction(PipelineAction)
```

This class implements a Transform action for an ETL pipeline.

The TransformConcatColumnsAction concats the given columns in a DataFrame.

<h4 id="actions.transform_concat_columns.TransformConcatColumnsAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        name: str = "",
        columns: list[str] | None = None,
        separator: str = "_",
        **_: Any) -> PipelineContext
```

Concats the columns for the given DataFrame.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `name` _str_ - Name of the new concatenated column.
- `columns` _list[str]_ - A list of columns that are concatenated.
- `separator` _str, optional_ - Separator used to concat columns. Defaults to "_"
  

**Raises**:

- `ValueError` - If no name is provided.
- `ValueError` - If no columns are provided.
- `ValueError` - If the data from context is None.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.consume_delta_load">actions.consume_delta_load</h1>

<h2 id="actions.consume_delta_load.ConsumeDeltaLoadAction">ConsumeDeltaLoadAction</h2>

```python
class ConsumeDeltaLoadAction(PipelineAction)
```

This class implements a Write action for an ETL pipeline.

The ConsumeDeltaLoadAction consumes a DeltaLoader transaction. It marks all DeltaLoad transactions currently in the runtime_info.

**Returns**:

  None.

<h4 id="actions.consume_delta_load.ConsumeDeltaLoadAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        delta_load_identifier: str | None = None,
        **_: Any) -> PipelineContext
```

Append the DataFrame to the delta table.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `delta_load_identifier` _str, optional_ - If set, the
  ConsumeDeltaLoadAction action will only consume DeltaLoader
  transaction for the given delta_load_identifier. Defaults to None.
  

**Returns**:

  Pipeline Context

<h1 id="actions.transform_rename_columns">actions.transform_rename_columns</h1>

<h2 id="actions.transform_rename_columns.TransformRenameColumnsAction">TransformRenameColumnsAction</h2>

```python
class TransformRenameColumnsAction(PipelineAction)
```

This class implements a Transform action for an ETL pipeline.

The TransformRenameColumnsAction renames the given columns in a DataFrame.

<h4 id="actions.transform_rename_columns.TransformRenameColumnsAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        columns: dict[str, str] | None = None,
        **_: Any) -> PipelineContext
```

Renames the columns for the given DataFrame.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `columns` _dict[str, str]_ - A Dict, where the key is the old name and
  the value is the new name of the column.
  

**Raises**:

- `ValueError` - If no columns are provided.
- `ValueError` - If the data from context is None.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.write_file">actions.write_file</h1>

<h2 id="actions.write_file.WriteFileAction">WriteFileAction</h2>

```python
class WriteFileAction(PipelineAction)
```

This class implements a Write action for an ETL pipeline.

The WriteFileAction write a Dataframe to a storage location defined in the
options.

<h4 id="actions.write_file.WriteFileAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        path: str = "",
        format: str = "delta",
        partition_cols: list[str] | None = None,
        mode: str = "append",
        is_stream: bool = False,
        options: dict[str, str] | None = None,
        **_: Any) -> PipelineContext
```

Writes a file to a location.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `path` _str_ - Location to write data to.
- `format` _str_ - Format of files to write. Default 'delta'.
- `partition_cols` _list[str]_ - Columns to partition on. If None, the
  writer will try to get the partition columns from the metadata.
  Default None.
- `mode` _str_ - Specifies the behavior when data or table already
  exists. Default 'append'.
- `is_stream` _bool_ - If True, use the `write_stream` method of the
  writer. Defaults to False.
- `options` _dict[str, str], optional_ - Additional options passed to the
  writer. Defaults to None.
  

**Raises**:

- `ValueError` - If no path is provided.
- `ValueError` - If the table metadata is empty.
  

**Returns**:

  Pipeline Context

<h1 id="actions.read_table_metadata_from_uc">actions.read_table_metadata_from_uc</h1>

<h2 id="actions.read_table_metadata_from_uc.ReadUnityCatalogTableMetadataAction">ReadUnityCatalogTableMetadataAction</h2>

```python
class ReadUnityCatalogTableMetadataAction(PipelineAction)
```

This class implements the option to infer table metadata from a UC table.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `table_identifier` _str_ - Identifier of the table in the format 'catalog.schema.table'.
  

**Raises**:

- `ValueError` - If no table identifier is provided.

<h4 id="actions.read_table_metadata_from_uc.ReadUnityCatalogTableMetadataAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        table_identifier: str | None = None,
        **_: Any) -> PipelineContext
```

Get table metadata from DataFrame using adapter.

<h1 id="actions.transform_convert_timestamp">actions.transform_convert_timestamp</h1>

<h2 id="actions.transform_convert_timestamp.TransformConvertTimestampAction">TransformConvertTimestampAction</h2>

```python
class TransformConvertTimestampAction(PipelineAction)
```

This class implements a Transform action for an ETL pipeline.

This action performs timestamp based conversions.

<h4 id="actions.transform_convert_timestamp.TransformConvertTimestampAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        column: str = "",
        source_format: str = "",
        target_format: str = "",
        **_: Any) -> PipelineContext
```

Converts a column from a given source format to a new format.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `column` _str_ - The column that should be converted.
- `source_format` _str_ - Initial format type of the column.
- `target_format` _str_ - Desired format type of the column. This also
  supports passing a format string like 'yyyy-MM-dd HH:mm:ss'.
  

**Raises**:

- `ValueError` - If no column, source_format and target_format are provided.
- `ValueError` - If source_format or target_format are not supported.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.read_files">actions.read_files</h1>

<h2 id="actions.read_files.ReadFilesAction">ReadFilesAction</h2>

```python
class ReadFilesAction(PipelineAction)
```

This class implements a Read action for an ETL pipeline.

The ReadFilesAction reads data from a source, defined by input variables and
returns a DataFrame.

<h4 id="actions.read_files.ReadFilesAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        path: str = "",
        search_subdirs: bool = False,
        extension: str | None = None,
        source_format: str | None = None,
        schema: str | None = None,
        include_source_file_column: bool = True,
        options: dict[str, str] | None = None,
        **_: Any) -> PipelineContext
```

Reads files from a path.

When given an extension, all files with the given extension will be
read. Otherwise the source_format must be set, then all files in the
path will be read using a DataFrameReader with the given format.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `path` _str_ - The path to read files from.
- `search_subdirs` _bool, optional_ - Search files recursively, when
  extension is set. Defaults to False.
- `extension` _str, optional_ - Extension of files to be included.
  Defaults to None.
- `source_format` _str, optional_ - Format of the DataFrameReader.
  Defaults to None.
- `schema` _str, optional_ - Schema of the data. If None,
  schema is read from context metadata.
- `include_source_file_column` _bool_ - Decides if the column
  `_source_file` is included, containing the file, where the data
  was read from. Defaults to False.
- `options` _dict[str, str], optional_ - Additional options passed to the
  reader. Defaults to None.
  

**Raises**:

- `ValueError` - Raised when neither extension nor source_format are
  defined.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.read_data_contract">actions.read_data_contract</h1>

<h2 id="actions.read_data_contract.ReadDataContractAction">ReadDataContractAction</h2>

```python
class ReadDataContractAction(PipelineAction)
```

This class implements a Read action to read ETL metadata.

The ReadDataContractAction reads metadata from a data contract on an
external volume, defined by input variables and returns the dataset metadata.

<h4 id="actions.read_data_contract.ReadDataContractAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        path: str | None = None,
        dataset_name: str | None = None,
        **_: Any) -> PipelineContext
```

Read data contract using the data contract service.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `path` _str_ - Path to the data contract.
- `dataset_name` _str_ - Name of the dataset for which to get metadata.
  

**Raises**:

- `ValueError` - If any errors occur while reading the data contract. E.g. if the schema
  is not valid or the path does not exist.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.transform_expand_columns">actions.transform_expand_columns</h1>

<h2 id="actions.transform_expand_columns.TransformExpandColumnsAction">TransformExpandColumnsAction</h2>

```python
class TransformExpandColumnsAction(PipelineAction)
```

This class implements a Transform action for an ETL pipeline.

The TransformExpandColumnsAction explodes and flattens values of an array or
struct column.

<h4 id="actions.transform_expand_columns.TransformExpandColumnsAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        exclude_columns: list[str] | None = None,
        explode_arrays: bool = True,
        flatten_structs: bool = True,
        recursive: bool = False,
        max_depth: int = -1,
        **_: Any) -> PipelineContext
```

Explodes and flattens all array and struct type columns in the DataFrame.

**Arguments**:

- `context` _PipelineContext_ - The context of the pipeline, containing
  the DataFrame to be transformed.
- `exclude_columns` _list[str], optional_ - A list of column names to
  exclude from the normalization process. These columns will not
  be exploded or flattened.
- `explode_arrays` _bool, optional_ - Decides if array type columns will
  be exploded. Defaults to True.
- `flatten_structs` _bool, optional_ - Decides if struct type columns
  will be flattened. Defaults to True.
- `recursive` _bool, optional_ - Decides if the exploding and flattening
  is performed recursively. Defaults to False.
- `max_depth` _int, optional_ - The maximum depth to which arrays and
  structs are exploded. Set to negative value to recurse
  indefinetely. Defaults to -1.
  

**Raises**:

- `ValueError` - If no column is specified or if the context data is
  None.

<h1 id="actions.transform_decode">actions.transform_decode</h1>

<h2 id="actions.transform_decode.TransformDecodeAction">TransformDecodeAction</h2>

```python
class TransformDecodeAction(PipelineAction)
```

This class implements a Transform action for an ETL pipeline.

The TransformDecodeAction decodes values of a column. Currently, it supports
decoding a column in base64 inplace, or expand a JSON column in place to new
columns.

<h4 id="actions.transform_decode.TransformDecodeAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        column: str = "",
        input_format: str = "",
        schema: str = "",
        field: str | None = None,
        **_: Any) -> PipelineContext
```

Decodes a column in a given format and returns the decoded DataFrame.

**Arguments**:

- `context` _PipelineContext_ - Context in which this Action is executed.
- `column` _str_ - Name of the column that should be decoded.
- `input_format` _str_ - Format from which the column should be decoded.
  Currently supported: 'base64', 'json'.
- `schema` _str_ - For json and json_list, schema of the json object. If empty, schema
  is inferred from the first row of the DataFrame. In json_list, the
  full json schema has to be given. For base64, datatype to which
  the column is cast.
- `field` _str_ - For json_list, field name of json field containing the
  list to be exploded.
  

**Raises**:

- `ValueError` - If no column is provided. ValueError: If the data from
  context is None.
  

**Returns**:

- `PipelineContext` - Context after the execution of this Action.

<h1 id="actions.read_api">actions.read_api</h1>

<h4 id="actions.read_api.process_auth">process_auth</h4>

```python
def process_auth(
    auth: Mapping[str, str | Mapping[str, str] | list[Mapping[str, str]]]
    | AuthBase | None
) -> AuthBase | None
```

Processes the auth parameter to create an AuthBase object.

**Arguments**:

- `auth` - The auth parameter to be processed.

<h2 id="actions.read_api.ReadAPIAction">ReadAPIAction</h2>

```python
class ReadAPIAction(PipelineAction)
```

Reads data from an API in parallel and writes the responses as JSON files.

**Example**:

```yaml
Read API:
    action: READ_API
    options:
        base_url: https://some_url.com/api/
        endpoint: my/endpoint/
        method: GET
        timeout: 90
        auth:
            - type: basic
              username: my_username
              password: my_password
            - type: secret_scope
              secret_scope: my_secret_scope
              header_template:
                "header_key_1": "<ENVIRONMENT_VARIABLE_NAME>"
            - type: secret_scope
              secret_scope: my_secret_scope
              header_template:
                "header_key_2": "<SECRET_NAME>"
            - type: secret_scope
              secret_scope: my_other_secret_scope
              header_template:
                "header_key_3": "<SECRET_NAME>"
            - type: azure_oauth
              client_id: my_client_id
              client_secret: my_client_secret
              tenant_id: my_tenant_id
              scope: <entra-id-client-id>
```
  
  The above example will combine the headers from the different auth types. The resulting header will look like this:
  
```json
{
    "header_key_1": "value_from_environment_variable",
    "header_key_2": "value_from_secret",
    "header_key_3": "value_from_secret",
    "Authorization": "Bearer <access_token> (from azure_oauth)",
    "Authorization": "Basic am9obkBleGFtcGxlLmNvbTphYmMxMjM= (from basic)"
}
```
  
  !!! warning
  
  Don't write sensitive information like passwords or tokens directly in the pipeline configuration.
  Use secret scopes or environment variables instead.

<h4 id="actions.read_api.ReadAPIAction.run">run</h4>

```python
def run(context: PipelineContext,
        *,
        base_url: str | None = None,
        auth: AuthBase | dict[str, str] | None = None,
        default_headers: dict[str, str] | None = None,
        endpoint: str = "",
        method: str = "GET",
        key: str | None = None,
        timeout: int = 30,
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        data: dict[str, str] | None = None,
        json_body: dict[str, str] | None = None,
        max_retries: int = 0,
        backoff_factor: int = 0,
        options: dict[str, str] | None = None,
        add_metadata_column: bool = False,
        max_workers: int = 10,
        save_path: str | None = None,
        requests_from_context: bool = False,
        raise_on_error: bool = True,
        **_: Any) -> PipelineContext
```

Executes API requests in parallel using ThreadPoolExecutor.

**Arguments**:

- `context` - The pipeline context containing information about the pipeline.
- `base_url` - The base URL for the API to be called.
- `auth` - Authentication credentials for the API.
- `default_headers` - Default headers to include in the API request.
- `endpoint` - The specific API endpoint to call.
- `method` - The HTTP method to use for the request (default is "GET").
- `key` - Key for accessing specific data in the response.
- `timeout` - Timeout for the API request in seconds.
- `params` - URL parameters for the API request.
- `headers` - Additional headers for the request.
- `data` - Data to send with the request for POST methods.
- `json_body` - JSON data to send with the request for POST methods.
- `max_retries` - Maximum number of retries for the API request.
- `backoff_factor` - Factor for exponential backoff between retries.
- `options` - Additional options for the API request.
- `add_metadata_column` - If set, adds a __metadata column with API response metadata.
- `max_workers` - Maximum number of threads for concurrent requests.
- `save_path` - Path of the file to permanently save JSON files for each request.
- `requests_from_context` - If set, the API requests are generated from the context.
- `raise_on_error` - If set, raises an exception if an error occurs during the request.
  

**Notes**:

  If `requests_from_context` is set to True, the `endpoint`,
  `query_parameters`, and `path_parameters` arguments will be ignored.
  The `context` DataFrame must contain one row per request with the
  following columns:
  - `endpoint`: The API endpoint to call.
  - `params`: URL parameters for the API request.
  - `body`: Data to send with the request for POST methods.
  - `full_save_path`: Path to save the JSON file for the request.
  

**Returns**:

  The updated pipeline context containing the DataFrame with API response data.

