# WinDEF Data Pipeline User Guide

WinDEF implements the capability to define, build and execute data pipelines. A
pipeline consists of a number of pipeline steps, that each execute a certain
action. Pipeline actions are common data actions in an ETL process, like reading
a file to a data frame, transforming a data frame, or merging a data frame to a
delta table. The pipeline actions are parametrized and can be configured to fit
your specific requirements. Most configuration can however be automatically be
determined from metadata in the data contract, which makes the WinDEF data
pipelines a very powerful tool.

Please refere to the [Pipeline Actions Documentation](./Pipeline/Pipeline-Actions.md) for
the currently implemented pipeline actions.

## Table of Content

- [WinDEF Data Pipeline User Guide](#windef-data-pipeline-user-guide)
  - [Table of Content](#table-of-content)
  - [Pipeline Context](#pipeline-context)
  - [How-to Configure a Data Pipeline](#how-to-configure-a-data-pipeline)
    - [Configure a Pipeline in YAML](#configure-a-pipeline-in-yaml)
      - [Referencing Secrets](#referencing-secrets)
      - [Example](#example)
    - [Configure a Pipeline in Code](#configure-a-pipeline-in-code)
  - [Pipeline Step Dependencies](#pipeline-step-dependencies)
  - [Reference](#reference)
    - [Pipeline Reference](#pipeline-reference)
    - [Pipeline Step Reference](#pipeline-step-reference)

## Pipeline Context

The WinDEF data pipeline keeps track of a `PipelineContext`, which contains the
data (a Spark `DataFrame`) and the metadata (a WinDEF `Table`). Each pipeline
action requires a `PipelineContext` as input and will return a
`PipelineContext`. The input and output context of an action is stored
in the pipeline step as `context` and `result`, respectively.

## How-to Configure a Data Pipeline

Data pipelines can be configured using YAML files or directly in code.

### Configure a Pipeline in YAML

The recommended method to configure data pipelines is through YAML files. These
files can be stored in the data product reposiory under the `etl` directory and
will be automatically picked up and deployed to the external volume `config` in
the data product schema by the `etl-metadata` pipeline.

> For a complete reference of the available pipeline actions, please refer to
> the [Referece section](#reference).

The layout of the YAML configuration for a data pipeline looks like this:

```yaml
id: <Name of the Pipeline>
env: <A dictionary of Environment Variables to be set in the context of the Pipeline>
    [ ... ]
steps: <A dictionary of Pipeline Steps>
    [ ... ]
```

The pipeline `id` is used in the logging. It should be descriptive of the pipeline
and contain a reference to your data product and the processed table.

A pipeline step has the following structure:

```yaml
<Name of the step (must be unique in a pipeline)>:
    action: <reference to the pipeline action>
    options: <a dictionary of parameters passed to the pipeline actions>
    [takes_input]: If the step should use the previous steps result as Input. Set to False, if the step should not take any input.
    [context]: The name of the step to get the context from.
    [metadata]: The name of the step to get the metadata from.
```

The name of the step is used in the logging. It is also used by the pipeline to
reference steps and obtain the resulting pipeline context.

For more details on the available pipeline actions, refere to the [Pipeline
Actions Guide](./Pipeline-Actions.md)

To build and run the pipeline in your Databricks notebook, you can simply use
the `PipelineParsingService`, which will parse the YAML file or a string
containing the YAML definition and return a `Pipeline` instance.

```python
from windef.pipeline import PipelineParsingService
# path to the YAML config file on an external volume
path = f"/Volumes/{os.environ.get('CATALOG_DATA_SOURCES')}/wdpf_testing/config/etl/test_table_1__landing_to_serving.yml"
# parse the file
pipeline = PipelineParsingService.parse_yaml(path=path)
# run the pipeline
pipeline.run()
```

> :bulb: It is recommended to read the pipeline definition YAML file
> directly from the data product "config" volume. If you are using the
> `etl-metadata` pipeline, you can find the YAML config file under
> `/Volumes/<catalog name>/<schema name>/config/etl/`. The catalog name can be
> easily obtained from the `CATALOG_DATA_SOURCES` and `CATALOG_DATA_PRODUCTS`
> environment variables, which are available on all clusters on WDAP.

#### Referencing Secrets

It is possible to reference secrets stored in a secret scope or in environment
variables in the YAML pipeline definition, so that you don't need to expose
secret values in a definition file.

A secret in a secret scope can be referenced using
`{{<secret_scope_name>:<secret_key>}}`. The YAML parsing service will then
obtain the secret from the secret scope and replace the reference, before
creating the pipeline action.

> :bulb: Note that you require permission to read secrets from the secret scope.

Similarly, an environment variable can be referenced using
`{{env:<variable_name>}}`. The YAML parsing service will replace the reference
with the value of that environment varialbe, before creating the pipeline
action.

Widgets can be referenced in the same manner as environment variables by using
`{{widget:<widget_name>}}`.

> :warning: This implies, that there cannot be a secret scope named "env" or "widget"!

#### Example

This is an example configuration for a pipeline that can bring CSV data from a
landing zone to a serving zone of a data source.

```yaml
id: Example Landing to Serving
env:
    WINDEF_LOG_TO_AZURE: True
steps:
    Read Table Metadata:
      action: READ_DATA_CONTRACT
      options:
        path: "/Volumes/{{env:CATALOG_DATA_SOURCES}}/wdpf_testing/config/data_contract"
        dataset_name: "test_table_1"

    Validate Table Metadata:
      action: VALIDATE_TABLE_METADATA
      options: {}

    Read Source:
      action: READ_FILES
      options:
        path: "{{ss-dbrks-external-location:ds-wdpf-testing}}/landing/test_table_1"
        extension: csv
        options:
          header: True

    Rename Columns:
      action: TRANSFORM_RENAME_COLUMN
      options:
        columns:
          pk_col: ID
          data_col: DATA
          email_col: EMAIL
          partition_col: FILE_ID

    Transform with SQL:
      action: TRANSFORM_SQL
      options:
        sql_statement: |
          SELECT ID, DATA, EMAIL, FILE_ID, DATA * FILE_ID as DERIVED_COLUMN
          FROM {DATA_FRAME}

    Validate Table:
      action: VALIDATE_TABLE_COLUMNS
      options: {}

    Write to Serving:
      action: WRITE_DELTA_MERGE
      options: {}
```

### Configure a Pipeline in Code

In addition to the YAML definition, it is also possible to define a data
pipeline as code in a Databricks notebook. This is especially useful when
developing a new data pipeline.

```python
from windef.pipeline import PipelineStep, ReadFilesAction, PipelineContext
pipeline = Pipeline("Test Pipeline")

step = PipelineStep(
            ReadFilesAction(),
            id="example step",
            context=PipelineContext(data=None, metadata=None),
            options={
                "path": "path/to/container/landing/test_table_1",
                "extension": "csv",
                "options": {"header": True},
            },
        )
pipeline.add(step)
pipeline.run()
```

## Pipeline Step Dependencies

Generally, the pipeline will execute the pipeline steps in the order in which
they are defined. In some cases it might however be required to explicitly
define dependencies of a pipeline step. This can be done using the `metadata`
and `context` keywords in the YAML configuration, or the `metadata_ref` and
`context_ref` parameters in the code definition of a pipeline step. The metadata
keywords will still get the context from the previous step, but replace the
metadata with the metadata obtained in a different step. The context keyword
will set the result context of the referenced step as context of this step.

In the following example, `step3` will get the context of `step1`:

```yaml
    id: example pipeline
    steps:
        step1:
            action: READ_FILES
        step2:
            action: READ_FILES
        step3:
            action: READ_FILES
            context: step1
```

In this example, `step3` will get the context of `step2` but the metadata of `step1`.

```yaml
    id: example pipeline 2
    steps:
        step1:
            action: READ_FILES
        step2:
            action: READ_FILES
        step3:
            action: READ_FILES
            metadata: step1
```

## Reference

### Pipeline Reference

| Option  | Required? | Description                                  | Example                                                                                                                  |
| ------- | --------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `id`    | Yes       | The name of the pipeline.                    | Example Pipeline                                                                                                         |
| `env`   | No        | A dictionary of environment keys and values. | {`"env_var_name":"env_var_value"}`                                                                                         |
| `steps` | Yes       | A dictionary of pipeline steps.              | See [Configure a Pipeline in YAML](#configure-a-pipeline-in-yaml) or [Pipeline Step Reference](#pipeline-step-reference) |

### Pipeline Step Reference

| Option        | Required? | Description                                                                                                                | Example                                                              |
| ------------- | --------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `id`          | Yes       | The name of the step.                                                                                                      | Read Table Metadata                                                  |
| `action`      | Yes       | The reference to the pipeline action.                                                                                      | READ_DATA_CONTRACT                                                   |
| `options`     | Yes       | A dictionary of parameters passed to the pipeline action. Can be an empty Dict, if the Action doesn't require any options. | See [Pipeline Actions Documentation](./Pipeline/Pipeline-Actions.md) |
| `metadata`    | no        | The name of the step to get the metadata from.                                                                             | Read Table Metadata                                                  |
| `context`     | no        | The name of the step to get the context from.                                                                              | Read Table Metadata                                                  |
| `takes_input` | no        | If the step should use the previous steps result as Input. Set to False, if the step should not take any input.            | True                                                                 |
