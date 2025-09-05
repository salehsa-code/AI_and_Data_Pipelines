# Data Contract

The data contract and corresponding dataset YAML definitions contain important
meta data describing the data product. The metadata can directly be used to
drive modules of the WinDEF package.

## Table of Contents

- [Data Contract Reference](#data-contract-reference)
  - [Datacontract Schema Reference](#datacontract-schema-reference)
  - [Datacontract Catalogue Record Reference](#datacontract-catalogue-record-reference)
  - [Datacontract Dataset Reference](#datacontract-dataset-reference)
  - [Example Datacontract Implementation](#example-datacontract-implementation)
- [Dataset Reference](#dataset-reference)
  - [Table Reference](#table-reference)
  - [Field Reference](#field-reference)
  - [Foreign Key Reference](#foreign-key-reference)
  - [Column Validation Reference](#column-validation-reference)
  - [Example Dataset Implementation](#example-dataset-implementation)

## Data Contract Reference

The data contract is a YAML file that contains the meta data of a data product onm schema level.

### Datacontract Schema Reference

| Field            | Type                              | Required | Comment                                   | Example                                                                                  |
| ---------------- | --------------------------------- | -------- | ----------------------------------------- | ---------------------------------------------------------------------------------------- |
| catalogue_record | DatacontractCatalogueRecordSchema | Yes      | Catalogue record associated with the data | See [Datacontract Catalogue Record Reference](#datacontract-catalogue-record-reference). |
| dataset          | DatacontractDatasetSchema         | Yes      | Dataset associated with the data          | See [Datacontract Dataset Reference](#datacontract-dataset-reference).                   |

### Datacontract Catalogue Record Reference

| Field         | Type      | Required | Comment                                                                                  | Example              |
| ------------- | --------- | -------- | ---------------------------------------------------------------------------------------- | -------------------- |
| primary_topic | str       | Yes      | The data product domain area and bounded context i.e. sub-capability and business object | topic                |
| modified      | date      | Yes      | Date when the record was modified. Use ISO-8601 as standard.                             | 2022-12-31           |
| keyword       | list[str] | Yes      | Keywords associated with the record, can be used to search the product.                  | [keyword1, keyword2] |

### Datacontract Dataset Reference

| Field             | Type              | Required | Comment                                                                                                 | Example                               |
| ----------------- | ----------------- | -------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| title             | str               | Yes      | A name given to the item                                                                                | title                                 |
| technical_title   | str               | Yes      | The name of data objects related to this contract (e.g. UC Schema)                                      | tech_title                            |
| data_product_type | str               | Yes      | Source, Primary (pristine) or Secondary (consumes primary data products)                                | source                                |
| description       | str               | Yes      | Description of the dataset                                                                              | Brief description of the data product |
| owner             | str               | Yes      | Owner of the dataset                                                                                    | Max Mustermann                        |
| owner_email       | EmailStr          | Yes      | Email of the owner                                                                                      | <max.mustermann@vattenfall.com>       |
| creator           | str               | Yes      | The entity responsible for producing the resource                                                       | Team Data Kong                        |
| issued            | date              | Yes      | Date when the dataset was issued. Use ISO-8601 as standard.                                             | 2022-12-31                            |
| modified          | date              | Yes      | Date when the dataset was modified. Use ISO-8601 as standard.                                           | 2022-12-31                            |
| publisher         | str               | Yes      | The entity responsible for making the item available                                                    | Vattenfall Wind BA - Offshore         |
| language          | str               | Yes      | Language of the dataset. Use the ISO-639 as a standard.                                                 | eng                                   |
| frequency         | str               | Yes      | The frequency at which dataset is published. Can be secondly, minutely, hourly, daily, weekly, monthly. | daily                                 |
| iac               | str \| None       | No       | IAC classification.                                                                                     | 2 GDPR low                            |
| version           | str               | Yes      | Version of the dataset                                                                                  | 1.0.0                                 |
| capability        | str \| None       | No       | Capability of the dataset                                                                               | Customer management                   |
| sub_capability    | str \| None       | No       | Sub-capability of the dataset                                                                           | Customer service                      |
| data              | list[str] \| None | No       | Data of the dataset                                                                                     | ["data1", "data2"]                    |

### Example Datacontract Implementation

```yaml
---
catalogue_record:
  primary_topic: "Data product domain area"
  modified: 2023-05-24
  keyword:
    - customer
    - gdpr
dataset:
  title: "Data product dataset name"
  technical_title: cable
  data_product_type: Primary
  description: "Brief description of the data product"
  owner: "Johan Olsson"
  owner_email: "johan.olsson@vattenfall.com"
  creator: "Data chef tribe A"
  issued: 2023-05-24
  modified: 2023-05-24
  publisher: "Vattenfall Wind BA - Business unit name"
  language: "eng"
  frequency: "hourly"
  iac: "2 GDPR low"
  version: "1.0.0"
  capability: "Customer management"
  sub_capability: "Customer service"
  data:
    - "table_name_1"
    - "table_name_2"
    - "table_name_3"
```

## Dataset Reference

The dataset is a YAML file that contains the meta data of a data product on table level.

### Table Reference

| Field               | Type   | Required | Comment                                                                                                                                                                                                                                                                  | Example                                                  |
| ------------------- | ------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------- |
| name                | String | Yes      | Name of the data object                                                                                                                                                                                                                                                  | cable_temperature                                        |
| business_name       | String | Yes      | Business description of the object                                                                                                                                                                                                                                       | Cable temperature                                        |
| description         | String | Yes      | A free-text account of the item                                                                                                                                                                                                                                          | Sensor data                                              |
| owner               | String | Yes      | Data product owner who owns the definition                                                                                                                                                                                                                               | Data Science Team                                        |
| partitioned_by      | String | Yes      | The column(s) by which data is partitioned                                                                                                                                                                                                                               | Date_SID                                                 |
| format              | String | Yes      | The file format of the distribution. Can be one of `delta`, `parquet`, `json`, `avro` and `csv`                                                                                                                                                                          | delta                                                    |
| fields              | Array  | Yes      | List of fields in the dataset, see [Field Reference](#field-reference)                                                                                                                                                                                                   | List of fields, see [Field Reference](#field-reference)] |
| foreign_keys        | list   | No       | A list of dictionaries containing [foreign_key_columns, parent_table, parent_columns, constraint_options and foreign_key_options](https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-create-table-constraint.html) for each foreign key in the table. | see FK reference below                                   |
| validation_rules    | Array  | No       | List of validations applied to the data on table level, see [DQX reference](https://databrickslabs.github.io/dqx/docs/reference/#quality-rule-functions-checks).                                                                                                                                                                                                                   | [ { "criticality": "error", "check": { "function": "sql_expression", "arguments": {"expression": "col1 LIKE '%foo'"}, }, "filter": "col1 IS NOT NULL",  } ]                                                    |

### Field Reference

| Field                  | Type    | Required | Comment                                                                                                                                                            | Example                                                  |
| ---------------------- | ------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------- |
| name                   | String  | Yes      | Name of the field                                                                                                                                                  | park_id                                                  |
| business_name          | String  | Yes      | Business-friendly name of the field                                                                                                                                | Park Id                                                  |
| description            | String  | Yes      | Description of the field                                                                                                                                           | Primary Key of the Wind Park                             |
| primary_key            | Boolean | Yes      | Indicates if the field is a primary key                                                                                                                            | false                                                    |
| data_type              | String  | Yes      | Data type of the field                                                                                                                                             | bigint                                                   |
| nullable               | Boolean | Yes      | Indicates if the field can have null values                                                                                                                        | false                                                    |
| field_source           | String  | Yes      | Source of the field                                                                                                                                                | assets                                                   |
| field_source_type      | String  | Yes      | Type of the source (e.g., table, view)                                                                                                                             | table                                                    |
| field_source_object    | String  | Yes      | Name of the source object                                                                                                                                          | substation                                               |
| field_source_attribute | String  | Yes      | Source attribute name                                                                                                                                              | park_id                                                  |
| identity               | Boolean | No       | Indicates if the field is an Identity, see [Databricks Reference](https://docs.databricks.com/en/delta/generated-columns.html#use-identity-columns-in-delta-lake). | false                                                    |
| default_value          | String  | No       | Default value of the field                                                                                                                                         | "a random string"                                        |
| sample_data            | Array   | No       | Sample data for the field                                                                                                                                          | ["1","2","3"]                                            |

### Foreign Key Reference

| Field                | Type   | Required | Comment                                                                                                                                                                                                                                     | Example                                              |
| -------------------- | ------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| foreign_key_columns  | list   | Yes      | List of column names in the table                                                                                                                                                                                                           | ["park_id", "another_id"]                            |
| parent_table         | String | Yes      | Identifier of the referenced table, '<env>' will be replaced with the actual environment during deployment. Backticks are used for escaping the name in Databricks.                                                                         | \`vap2_<env>_wdap_dataproducts\`.\`assets\`.\`park\` |
| parent_table_columns | String | Yes      | List of column names in the referenced table                                                                                                                                                                                                | ["park_id", "another_id"]                            |
| constraint_options   | String | No       | `NOT ENFORCED`, `DEFERRABLE`, `INITIALLY DEFERRED`, `NORELY`, `RELY`, see [Databricks Reference](https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-alter-table-add-constraint.html) for the full list and descriptions. | NORELY NOT ENFORCED                                  |
| foreign_key_options  | String | No       | `MATCH FULL`, `ON UPDATE NO ACTION` or `ON DELETE NO ACTION`, see [Databricks Reference](https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-alter-table-add-constraint.html) for the full list and descriptions.         | MATCH FULL                                           |

### Column Validation Reference

| Field    | Type   | Required | Comment                                                                                      | Example                 |
| -------- | ------ | -------- | -------------------------------------------------------------------------------------------- | ----------------------- |
| name     | String | Yes      | Name of the validation rule                                                                  | COLUMN_IS_DATATYPE      |
| severity | String | Yes      | Severity of the validation, one of `notset`, `debug`, `info`, `warning`, `error`, `critical` | "error"                 |
| **kwargs | String | No       | Additional keywords for the validation rule                                                  | {"data_type": "bigint"} |

### Example Dataset Implementation

```yaml
name: "cable_temperature"
business_name: "Cable temperature"
description: "Sensor data"
owner: "Data Science Team"
partitioned_by: "Date_SID"
format: "delta"
foreign_keys:
    - foreign_key_columns: ["park_id"]
      parent_table: "`vap2_<env>_wdap_dataproducts`.`assets`.`park`"
      parent_columns:
          - "park_id"
      constraint_options: "NORELY NOT ENFORCED"
      foreign_key_options: "MATCH FULL"
fields:
  - name: "park_id"
    business_name: "Park Id"
    description: "Foreign key of the Wind Park"
    primary_key: false
    data_type: "bigint"
    nullable: false
    default_value: ""
    field_source: "assets"
    field_source_type: "table"
    field_source_object: "substation"
    field_source_attribute: "park_id"
    sample_data:
      - "1"
      - "2"
      - "3"
validation_rules:
    - criticality: error
      check:
        function: is_not_null
        arguments:
          col_name: ID
    - criticality: error
      check:
        function: is_in_range
        arguments:
          col_name: DATA
          min_limit: -10000
          max_limit: 10000
    - criticality: error
      check:
        function: regex_match
        arguments:
          col_name: EMAIL
          regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
```
