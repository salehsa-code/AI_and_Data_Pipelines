# Pipeline Actions

Pipeline Actions provide an efficient way to perform various actions in an ETL
pipeline. An action encapsulates the capabilities of a part of WinDEF to be used
in a Pipeline. This package provides a flexible and powerful way to define and
perform ETL tasks. It allows for easy addition of new actions and adjustments to
existing ones.

It is structured around the `PipelineAction` class, which is further subclassed
into various specific actions. These subclasses define different actions that
can be performed on data during an ETL process, including e.g.:

1. Reading data and metadata
2. Transforming data
3. Validating data and metadata
4. Writing data

## Concept

The `PipelineAction` is the parent class for all actions. It provides a
structure for defining specific actions. Each specific action is a subclass of
`PipelineAction` and implements a `run` method that describes how the action
should be executed.

A key concept in this package is the `PipelineContext` object. It encapsulates
the state of the pipeline at any given point and is passed between different
pipeline actions. It contains metadata and the data to be processed.

The `PipelineActionType` is an enumeration that dynamically registers all
subclasses of `PipelineAction` defined in this submodule. It uses their "name"
attribute as key for easy identification and usage.

## Usage

PipelineActions are meant to be used in WinDEF-Pipelines. Each `PipelineStep` is
assigned an Action. The Action then gets the context from the `PipelineStep` and
executes accordingly.

Remember that each action returns a new `PipelineContext` that contains the
updated state of the pipeline.

## List-of-Actions with brief description

| Action                                                                                       | Description                                                                                                                                                                    | Additional Docs                                  |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| [CREATE_DELTA_TABLE](../../../Reference/pipeline.md#actions.create_table)                     | Create a Delta Table                                                                                                                                                           | -                                                 |
| [EXECUTE_SQL](../../../Reference/pipeline.md#actions.execute_sql)                             | Execute arbitrary SQL statements. These statements do NOT alter the data in the context. They can be used to execute arbitrary SQL, e.g. to create views or alter permissions. | -                                                 |
| [MOVE_FILES](../../../Reference/pipeline.md#actions.move_file)                                | Move files from one location to another.                                                                                                                                       | -                                                 |
| [LIST_FILES](../../../Reference/pipeline.md#actions.list_files)               | List files in a directory and return a DataFrame with the file paths.                                                                                                                          | -                                                 |
| [READ_DATA_CONTRACT](../../../Reference/pipeline.md#actions.read_data_contract)               | The ReadDataContractAction reads metadata from a data contract on an external volume, defined by input variables and returns the dataset metadata.                             | -                                                 |
| [READ_TABLE](../../../Reference/pipeline.md#actions.read_delta_table)                         | Reads data from a delta table.                                                                                                                                                 | -                                                 |
| [READ_EXCEL](../../../Reference/pipeline.md#actions.read_excel)                               | Reads data from an Excel file.                                                                                                                                                 | -                                                 |
| [READ_FILES_STREAM](../../../Reference/pipeline.md#actions.read_files_stream)                 | Streams data from a source. :warning: Streaming is experimental and comes with some limitations.                                                                               | -                                                 |
| [READ_FILES](../../../Reference/pipeline.md#actions.read_files)                               | Reads data from files.                                                                                                                                                         | -                                                 |
| [READ_DATAFRAME_METADATA](../../../Reference/pipeline.md#actions.read_table_metadata)         | Infer table metadata from a DataFrame.                                                                                                                                         | -                                                 |
| [RUN_NOTEBOOK](../../../Reference/pipeline.md#actions.run_notebook_action)                    | Run a notebook. This allows to run arbitrary code in a notebook. It involves some overhead and should be used sparingly, e.g. if WinDEF does not provide a specific action.    | [here](./Pipeline-Actions./Run-Notebook-Action.md)|
| [TRANSFORM_ADD_COLUMN](../../../Reference/pipeline.md#actions.transform_add_column)           | Add a set of columns, initialized with a literal value.                                                                                                                        | -                                                 |
| [TRANSFORM_CHANGE_DATATYPE](../../../Reference/pipeline.md#actions.transform_change_datatype) | Change the datatype of one or more columns.                                                                                                                                    | -                                                 |
| [TRANSFORM_CONCAT_COLUMNS](../../../Reference/pipeline.md#actions.transform_concat_columns)   | Concatenate a list of columns with a separator.                                                                                                                                | -                                                 |
| [TRANSFORM_DECODE](../../../Reference/pipeline.md#actions.transform_decode)                   | Decode a column. Currently, it supports decoding a column in base64 inplace, or expand a JSON column in place to new columns.                                                  | -                                                 |
| [TRANSFORM_DISTINCT](../../../Reference/pipeline.md#actions.transform_distinct)               | Remove duplicates from a DataFrame.                                                                                                                                            | -                                                 |
| [TRANSFORM_FILTER](../../../Reference/pipeline.md#actions.transform_filter)                   | Filter a DataFrame by defining a condition.                                                                                                                                    | -                                                 |
| [TRANSFORM_SQL](../../../Reference/pipeline.md#actions.transform_sql)                         | Execute arbitrary SQL statements on a DataFrame.                                                                                                                               | -                                                 |
| [TRANSFORM_JOIN](../../../Reference/pipeline.md#actions.transform_join)                       | Join two DataFrames.                                                                                                                                                           | -                                                 |
| [TRANSFORM_RENAME_COLUMNS](../../../Reference/pipeline.md#actions.transform_rename_columns)   | Rename columns in a DataFrame.                                                                                                                                                 | -                                                 |
| [TRANSFORM_REPLACE_VALUES](../../../Reference/pipeline.md#actions.transform_replace_values)   | Replace values in a DataFrame.                                                                                                                                                 | -                                                 |
| [TRANSFORM_SELECT_COLUMNS](../../../Reference/pipeline.md#actions.transform_select_columns)   | Select columns in a DataFrame. Either by including or excluding columns.                                                                                                       | -                                                 |
| [TRANSFORM_UNION](../../../Reference/pipeline.md#actions.transform_union)                     | Union two or more DataFrames.                                                                                                                                                  | -                                                 |
| [VALIDATE_TABLE_COLUMNS](../../../Reference/pipeline.md#actions.validate_table)               | Validate the columns of a DataFrame based on the schema definition.                                                                                                            | -                                                 |
| [WRITE_DELTA_APPEND_STREAM](../../../Reference/pipeline.md#actions.write_delta_table_stream)  | Streaming data to a Delta table. :warning: Streaming is experimental and comes with some limitations.                                                                          | -                                                 |
| [WRITE_DELTA_APPEND](../../../Reference/pipeline.md#actions.write_delta_table)                | Append data to a Delta table.                                                                                                                                                  | -                                                 |
| [WRITE_DELTA_MERGE](../../../Reference/pipeline.md#actions.write_delta_table)                 | Merge data into a Delta table.                                                                                                                                                 | -                                                 |
| [WRITE_FILE](../../../Reference/pipeline.md#actions.write_file)                               | Write data to a file. Allows for streaming, but be aware of the limitations.                                                                                                   | -                                                 |
