# Table of Contents

* [validation\_config](#validation_config)
* [quarantine\_table](#quarantine_table)
* [exceptions](#exceptions)
* [quarantine\_service](#quarantine_service)
* [validation\_runner](#validation_runner)

<h1 id="validation_config">validation_config</h1>

<h2 id="validation_config.ValidationConfig">ValidationConfig</h2>

```python
class ValidationConfig(BaseModel)
```

Configuration to validate data.

**Arguments**:

  quarantine_catalog (optional(str)): The catalog containing the
  quarantine data. Can be None, if data is not quarantined.
  quarantine_schema (optional(str)): The schema containing the
  quarantine data. Will be derived from 'WINDEF__Q_SCHEMA' if not
  given explicitly. Default is 'quarantine'.
  quarantine_header_table_name (optional(str)): The name of the
  quarantine header table. Will be derived from 'WINDEF__Q_QUARANTINE_HEADER_TABLE'
  if not given explicitly. Default is 'quarantine_header'.
  quarantine_records_table_name (optional(str)): The name of the
  quarantine records table. Will be derived from 'WINDEF__Q_QUARANTINE_RECORDS_TABLE'
  if not given explicitly. Default is 'quarantine_records'.
  validation_rules (optional(list[dict[str, str]])): The validation
  rules to apply. Default is None.
  target_table (optional(str)): The target table to validate. Default
  is None.
  pipeline_id (optional(str)): The WinDEF pipeline id. Default is None.
  job_id (optional(str)): The WinDEF job id. Default is None.
  quarantine_invalid_data (optional(bool)): Whether to quarantine
  invalid data. Default is True.
  raise_on_criticality (optional(str)): The level of violation that must
  fail, before the runner raises a ValidationException. Defaults
  to 'error'. Accepts 'error' and 'warn'.
  exclude_warnings (optional(bool)): Whether to exclude warnings from
  the validation results. Default is False.

<h2 id="validation_config.ValidationConfig.Config">Config</h2>

```python
class Config()
```

Pydantic configuration.

<h4 id="validation_config.ValidationConfig.validate_validation_rules">validate_validation_rules</h4>

```python
@field_validator("validation_rules")
@classmethod
def validate_validation_rules(
    cls, validation_rules: list[dict[str, str | dict[str, str]]] | None
) -> list[dict] | None
```

Validate the validation_rules.

<h4 id="validation_config.ValidationConfig.quarantine_header_table">quarantine_header_table</h4>

```python
@property
def quarantine_header_table() -> str
```

Return the full name of the quarantine header table.

<h4 id="validation_config.ValidationConfig.quarantine_records_table">quarantine_records_table</h4>

```python
@property
def quarantine_records_table() -> str
```

Return the full name of the quarantine records table.

<h1 id="quarantine_table">quarantine_table</h1>

<h2 id="quarantine_table.QuarantineHeaderTable">QuarantineHeaderTable</h2>

```python
class QuarantineHeaderTable(Table)
```

A Table Model for the Quarantine Header Table.

<h2 id="quarantine_table.QuarantineRecordsTable">QuarantineRecordsTable</h2>

```python
class QuarantineRecordsTable(Table)
```

A Table Model for the Quarantine Records Table.

<h1 id="exceptions">exceptions</h1>

<h2 id="exceptions.ValidationException">ValidationException</h2>

```python
class ValidationException(Exception)
```

When a configuration validation fails.

<h1 id="quarantine_service">quarantine_service</h1>

<h2 id="quarantine_service.QuarantineService">QuarantineService</h2>

```python
class QuarantineService()
```

Service to quarantine data based on a configuration.

<h4 id="quarantine_service.QuarantineService.quarantine">quarantine</h4>

```python
def quarantine(data: DataFrame) -> None
```

Quarantine data based on a configuration.

<h1 id="validation_runner">validation_runner</h1>

<h2 id="validation_runner.ValidationRunner">ValidationRunner</h2>

```python
class ValidationRunner(BaseModel)
```

A class that runs validators for a given Table object.

<h4 id="validation_runner.ValidationRunner.configuration">configuration</h4>

| dict[str, str] | Path | str | Any

<h4 id="validation_runner.ValidationRunner.validate_configuration">validate_configuration</h4>

```python
@field_validator("configuration", mode="before")
@classmethod
def validate_configuration(
        cls, data: Path | str | ValidationConfig | dict[str, str]
) -> ValidationConfig
```

Validate the configuration.

<h4 id="validation_runner.ValidationRunner.model_post_init">model_post_init</h4>

```python
def model_post_init(__context: Any) -> None
```

Post init hook for the BaseModel.

<h4 id="validation_runner.ValidationRunner.validate_data">validate_data</h4>

```python
def validate_data(df: DataFrame) -> DataFrame
```

Validates a DataFrame using all validators in this runner.

**Arguments**:

- `df` _DataFrame_ - The DataFrame to validate.
  

**Returns**:

- `DataFrame` - The DataFrame with the valid rows, potentially including warnings.
  

**Raises**:

- `ValidationException` - If any of the validations fail.

