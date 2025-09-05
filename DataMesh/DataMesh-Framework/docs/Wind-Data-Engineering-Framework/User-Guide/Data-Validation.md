# Data Validation

## Overview

The Data Validation module is used to validate the actual data of a Table or
Column. It will check if the data is valid and consistent according to checks
defined in the data contract. The Validators, e.g. have checks whether the data
is in a given range or of a given datatype.

The Validation implements an abstraction on top of the [DQX
Framework](https://databrickslabs.github.io/dqx/), which is developed by
Databricks.

## Configuration

The Data Validation module can be configured using a combination of parameters
and environment variables. Below is a detailed list of all possible
configuration options and their default values.

### Parameters

- **quarantine_catalog**: (optional, str) The catalog containing the quarantine
  data. This is required if `quarantine_invalid_data` is set to True. Default is
  None.
- **quarantine_schema**: (optional, str) The schema containing the quarantine
  data. Will be derived from `WINDEF__Q_SCHEMA` if not given explicitly. Default
  is quarantine.
- **quarantine_header_table_name**: (optional, str) The name of the quarantine
  header table. Will be derived from `WINDEF__Q_QUARANTINE_HEADER_TABLE` if not
  given explicitly. Default is quarantine_header.
- **quarantine_records_table_name**: (optional, str) The name of the quarantine
  records table. Will be derived from `WINDEF__Q_QUARANTINE_RECORDS_TABLE` if
  not given explicitly. Default is quarantine_records.
- **validation_rules**: (optional, list[dict[str, str]]) The validation rules to
  apply. Default is None.
- **target_table**: (optional, str) The target table the validated data is
  supposed to be written to. Default is None.
- **pipeline_id**: (optional, str) The WinDEF pipeline id. Default is None.
- **job_id**: (optional, str) The Databricks Job id. Default is None.
- **quarantine_invalid_data**: (optional, bool) Whether to quarantine invalid
  data. Default is True.
- **raise_on_criticality**: (optional, str) The level of violation that must
  fail before the runner raises a `ValidationException`. Defaults to `error`.
  Accepts `error` and `warn`.
- **exclude_warnings**: (optional, bool) If set to true, the returned DataFrame
  will exclude validated records, that contain warnings. Defaults to False.

### Environment Variables

Some information that is written to the quarantine tables is derived or
configured by environment variables.

| Variable                             | Parameter                       | Description                                                                                                                                                                  |
| ------------------------------------ | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `WINDEF__Q_SCHEMA_NAME`              | `quarantine_schema_name`        | Name of the quarantine schema.                                                                                                                                               |
| `WINDEF__Q_QUARANTINE_HEADER_TABLE`  | `quarantine_header_table_name`  | Name of the Quarantine Header table.                                                                                                                                         |
| `WINDEF__Q_QUARANTINE_RECORDS_TABLE` | `quarantine_records_table_name` | Name of the Quarantine Records table.                                                                                                                                        |
| `WINDEF__PIPELINE_ID`                | `pipeline_id`                   | WinDEF Pipeline Id of the current pipeline. This environment variable is automatically set by the pipeline when a run starts.                                                |
| `DBRKS_JOB_ID`                       | `job_id`                        | Job Id of the current job. This should be set in the job using [dynamic job parameters](https://learn.microsoft.com/en-us/azure/databricks/jobs/parameter-value-references). |

## How To Run the Validator

To run the validator, first get the validator object and initialize the
validation runner with a config.

```python
from windef.validation import DataValidationRunner

validation_config = {
    "quarantine_catalog": "catalog",
    "quarantine_schema": "schema",
    "quarantine_header_table_name": "quarantine_headers",  # information about the run
    "quarantine_records_table_name": "quarantine_records",  # information about the data, join via id to headers
    "target_table": "catalog.schema.target_table",
    "validation_rules": [
        {
            "criticality": "error",  # can be either 'error' or 'warn'
            "check": {
                "function": "sql_expression",  # see below for a link to the reference
                "arguments": {"expression": "col1 LIKE '%foo'"},
            },
            "filter": "col1 IS NOT NULL",  # records to exclude from the test
        },
    ],
}

data_validation_runner = DataValidationRunner(configuration=validation_config)

df = spark.table(data_to_validate)  # the DataFrame you want to validate
data_validation_runner.validate_data(df)
```

A full list of Validators can be taken from [the DQX
Reference](https://databrickslabs.github.io/dqx/docs/reference/). In WinDEF,
these would typically be derived from the data contract.

## Validation Action

The [pipeline action](./Pipeline/Pipeline-Actions.md) `VALIDATE_TABLE_COLUMNS`
is used to run data validation checks within a WinDEF pipeline. The pipeline
action automatically reads the validation configuration from the metadata
context and runs all validators. Additionally, it allows to send invalid data
into a quarantine table.

The action can, e.g. be defined as follows:

```yaml
Validate Table:
    action: VALIDATE_TABLE_COLUMNS
    options:
        quarantine_invalid_data: True
        raise_on_criticality: error
        quarantine_catalog: catalog_name
        quarantine_schema_name: schema_name
        quarantine_header_table_name: "header_quarantine"
        quarantine_records_table_name: "records_quarantine"
```

### Quarantine Mechanism

Invalid records in the data with a criticality of

- `error` are removed from the DataFrame in the context and written to the
  quarantine table. The pipeline will exit with an error.
- `warn` are kept in the DataFrame, and additionnaly written to the quarantine
  table. The pipeline will exit with an error, if `raise_on_criticality` is set
  to `warn`

By default the `quarantine_header` and `quarantine_records` tables in the
`quarantine` schema of the configured `quarantine_catalog` are used. This
behavior can be changed, by configuring the `quarantine_schema_name`,
 `quarantine_header_table_name` and `quarantine_records_table_name`parameters of
the pipeline action, or by setting appropriate environment variables (see
below).

The quarantine mechanism can be disabled by setting the
`quarantine_invalid_data` parameter of the pipeline action to `False`.

The quarantine header table has the following format:

| Column Name   | Data Type | Description                                  |
| ------------- | --------- | -------------------------------------------- |
| id            | bigint    | Primary key, identity column                 |
| timestamp_utc | timestamp | The timestamp of the invalidation in UTC     |
| pipeline_id   | string    | Identifier for the WinDEF pipeline, nullable |
| job_id        | string    | Identifier for the Databricks job, nullable  |
| target_table  | string    | Name of the target table, nullable           |

The quarantine records table has the following format:

| Column Name          | Data Type | Description                                                                             |
| -------------------- | --------- | --------------------------------------------------------------------------------------- |
| id                   | bigint    | Primary key, identity column                                                            |
| quarantine_header_id | bigint    | Unique identifier for the referenced record in the quarantine header table, foreign key |
| record               | string    | The record that was quarantined as JSON object                                          |
| validation_error     | string    | The validation error message                                                            |
