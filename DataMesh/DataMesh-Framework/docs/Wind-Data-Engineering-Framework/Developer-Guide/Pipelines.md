# Pipelines

The Pipelines Framework is the most abstract implementation of utility blocks in
WinDEF. It allows users and developers to define ETL/ELT-Pipelines to be defined
as YAML.

## Pipeline Definition

This is the Reference for the Pipeline definition:

```yaml
<id>: str
<steps>: list[PipelineStep]
```

This is the Reference for the PipelineStep definition:

```yaml
<str>:  # humand readable name, serves as ID
    action: <str>  # name of the Action from PipelineActionType
    [takes_input]: <bool>  # If not specified or False, the predecessor will be defined as context_ref
    [context]: <str>  # Name of the step to refer to for the Context (Metadata & Data)
    [metadata]: <str>  # Name of the step to refer to for the Metadata
    [options]:  # Optional list of options to be passed to the PipelineAction instance (passed as **kwargs)
```

All options and keys support string replacement with either environment
variables `${env:ENV_VARIABLE_NAME}` or secrets from a secret scope `{{secret_scope_name:secret_name}}`.

In this example, the option `client_secret` will be replaced by the secret `client-secret`
from the secret scope named `atm-key-vault-ss`.

```yaml
id: Example Pipeline
steps:
  Read Secret API:
    action: READ_API
      options:
        client_id: 12345
        client_secret: {{atm-key-vault-ss:client-secret}}
```
