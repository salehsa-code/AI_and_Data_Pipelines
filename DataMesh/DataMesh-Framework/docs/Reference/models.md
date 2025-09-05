# Table of Contents

* [external\_location](#external_location)
* [schema](#schema)
* [foreign\_key](#foreign_key)
* [catalog](#catalog)
* [base\_model](#base_model)
* [environment](#environment)
* [column](#column)
* [table](#table)
* [adapter](#adapter)
* [adapter.unity\_catalog\_adapter](#adapter.unity_catalog_adapter)
* [adapter.dataframe\_adapter](#adapter.dataframe_adapter)
* [data\_contract](#data_contract)
* [data\_contract.data\_contract](#data_contract.data_contract)
* [data\_contract.dataset](#data_contract.dataset)

<h1 id="external_location">external_location</h1>

<h2 id="external_location.ExternalLocationPath">ExternalLocationPath</h2>

```python
class ExternalLocationPath()
```

A class representing a path on an External Location.

<h4 id="external_location.ExternalLocationPath.from_external_location_path">from_external_location_path</h4>

```python
@classmethod
def from_external_location_path(
        cls, external_location_path: str) -> "ExternalLocationPath"
```

Create an ExternalLocationPath from a path string.

<h4 id="external_location.ExternalLocationPath.get_path">get_path</h4>

```python
def get_path()
```

Returns the external location path as a string.

<h1 id="schema">schema</h1>

<h2 id="schema.Schema">Schema</h2>

```python
class Schema(WinDefModel, BaseModel)
```

A class that represents a database schema with a name and a list of tables.

**Attributes**:

- `name` _str_ - The name of the schema.
- `catalog` _str_ - The catalog of the schema.
- `tables` _List[Table]_ - A list of Table objects that make up the schema.
- `title` _str_ - The title used in Alation. Defaults to "".
- `comment` _str_ - A comment displayed in Alation as non-editable. Defaults to "".
- `description` _str_ - A description of the data in this schema. Defaults to "".
- `owner_email` _str_ - Email adress of the Data Owner. Defaults to "".

<h4 id="schema.Schema.environment">environment</h4>

```python
@property
def environment() -> Environment
```

The environment of the schema.

<h4 id="schema.Schema.metadata_to_instance">metadata_to_instance</h4>

```python
@classmethod
def metadata_to_instance(
        cls, data: dict) -> tuple[Schema | None, list[ValidationError]]
```

Parses a Dictionary to an instance.

**Arguments**:

- `data` - The dictionary to parse to an instance.
  

**Returns**:

  An instance and potentially a list of errors.

<h4 id="schema.Schema.read_instance_from_file">read_instance_from_file</h4>

```python
@classmethod
def read_instance_from_file(
    cls, instance_path: pathlib.Path
) -> tuple[Schema | None, list[ValidationError | yaml.parser.ParserError
                               | yaml.scanner.ScannerError]]
```

Read and instantiate a single YAML file for the given path.

**Arguments**:

- `instance_path` - The path to the file to instantiate.
- `key` - The key to read from the dictionary.
  

**Raises**:

- `ValueError` - If any errors occur while reading the data contract.
- `ValueError` - If no schema could be instantiated from the data contract.
  

**Returns**:

  Returns a tuple of the instantiated model and errors.

<h4 id="schema.Schema.add_tables">add_tables</h4>

```python
def add_tables(tables: list[Table]) -> None
```

Adds tables to the schema.

**Arguments**:

- `tables` _list[Table]_ - A list of Table objects that are added to the Schema tables.

<h4 id="schema.Schema.add_table">add_table</h4>

```python
def add_table(table: Table)
```

Adds a table to the schema and sets the table identifier accordingly.

**Arguments**:

- `table` _Table_ - A Table object that is added to the Schema tables.

<h4 id="schema.Schema.get_table_by_name">get_table_by_name</h4>

```python
def get_table_by_name(table_name: str) -> Table
```

Gets a table from the schema by its name.

**Arguments**:

- `table_name` _str_ - The name of the table to be retrieved.
  

**Returns**:

- `Table` - The table with the given name.

<h1 id="foreign_key">foreign_key</h1>

<h2 id="foreign_key.ForeignKey">ForeignKey</h2>

```python
class ForeignKey(BaseModel)
```

This class represents a Foreign Key Relationship with another Table in Unity Catalog.

<h4 id="foreign_key.ForeignKey.constraint_options">constraint_options</h4>

with our current setup these don't seem to work - revist when needed

<h4 id="foreign_key.ForeignKey.fk_options">fk_options</h4>

with our current setup these don't seem to work - revist when needed

<h4 id="foreign_key.ForeignKey.get_alter_table_string">get_alter_table_string</h4>

```python
def get_alter_table_string(table_identifier: str) -> str
```

Returns the ALTER TABLE statement to add the Foreign Key constraint.

**Arguments**:

- `table_identifier` _str_ - The identifier of the Table to apply the constraint on.
  

**Raises**:

- `ValueError` - If the parent_table_columns of the FK are neither string nor list.
  

**Returns**:

- `str` - The ALTER TABLE statement.

<h1 id="catalog">catalog</h1>

<h2 id="catalog.Catalog">Catalog</h2>

```python
@dataclass
class Catalog(WinDefModel)
```

A class representing a Unity Catalog - Catalog.

<h1 id="base_model">base_model</h1>

<h2 id="base_model.WinDefModel">WinDefModel</h2>

```python
class WinDefModel()
```

Abstract base model.

<h1 id="environment">environment</h1>

<h2 id="environment.EnvironmentProperties">EnvironmentProperties</h2>

```python
class EnvironmentProperties()
```

The properties of an environment.

<h2 id="environment.Environment">Environment</h2>

```python
class Environment(Enum)
```

The environment.

<h4 id="environment.Environment.name">name</h4>

```python
@property
def name()
```

The long name of the environment.

<h4 id="environment.Environment.long_name">long_name</h4>

```python
@property
def long_name()
```

The long name of the environment.

<h4 id="environment.Environment.catalogs">catalogs</h4>

```python
@property
def catalogs()
```

The catalogs of the environment.

<h4 id="environment.Environment.storage_accounts">storage_accounts</h4>

```python
@property
def storage_accounts()
```

The storage accounts of the environment.

<h4 id="environment.Environment.from_table_identifier">from_table_identifier</h4>

```python
@staticmethod
def from_table_identifier(table_identifier: str)
```

Return the environment from the table identifier.

<h1 id="column">column</h1>

<h2 id="column.Column">Column</h2>

```python
class Column(WinDefModel, BaseModel)
```

A class that represents a column in a table.

**Attributes**:

- `name` _str_ - The name of the column.
- `data_type` _str_ - The data type of the column.
- `pk` _bool_ - Whether the column is a primary key.
- `nullable` _bool_ - Whether the column can have null values.
- `default_value` _str_ - The default value of the column.
- `comment` _str_ - A comment for the column.
- `identity` _bool_ - Whether the column is an identity column.
- `business_properties` _Dict[str, Any]_ - A collection of attributes that are used in
  business related contexts, such as Alation or Graph Database.

<h4 id="column.Column.get_column_string">get_column_string</h4>

```python
def get_column_string() -> str
```

Get a string representation of the column.

**Returns**:

- `str` - A string representation of the column.

<h4 id="column.Column.__eq__">__eq__</h4>

```python
def __eq__(__value: object) -> bool
```

Checks if the current object is equal to the given object.

This method overrides the built-in `__eq__` method to provide a custom equality check for the Column class.
Two Column objects are considered equal if all their corresponding attributes ('name', 'data_type', 'pk',
'nullable', 'default_value', 'identity') are equal.

<h1 id="table">table</h1>

<h2 id="table.Table">Table</h2>

```python
class Table(WinDefModel, BaseModel)
```

A class representing a table in Unity Catalog, providing utilities for validation and DDL creation.

This class encapsulates information about a table in the Unity Catalog
system. It includes necessary details required for creating a DDL statement
for the table. Furthermore, it offers utility methods to validate the table
definition, ensuring it meets the necessary criteria and constraints.

**Attributes**:

- `name` _str_ - The name of the table.
- `format` _str_ - The format of the table.
- `columns` _List[Column]_ - A list of Column objects that make up the table's structure.
- `foreign_keys` _List[ForeignKey]_ - A list of foreign key objects applied on the table.
  partitioned_by (List(Column), List(str)): The column names by which the table is
  partitioned using either liquid clustering or partitioning. Defaults to None.
- `comment` _str_ - A comment for the table.
- `location` _str_ - The location of the table. If specified the table is treated
  as "EXTERNAL TABLE" in Unity Catalog.
- `use_liquid_clustering` _bool_ - Use liquid clustering. Defaults to true,
  requires Databricks Runtime 13.3 LTS or above.
- `identifier` _str_ - The identifier to reference the table. Combination of
  catalog, schema and table names.
- `business_properties` _Dict[str, Any]_ - A collection of attributes that are used in
  business related contexts, such as Alation or Graph Database.
- `validation_rules` _List[Dict[str, Any]]_ - A list of validation rules to be applied to the data.
  Defaults to None. Define according to DQX standards.
  
  Properties:
- `schema` _str_ - The schema of the table.
- `catalog` _str_ - The catalog of the table.
- `primary_key` _str_ - The primary key of the table.

<h4 id="table.Table.read_instances_from_directory">read_instances_from_directory</h4>

```python
@classmethod
def read_instances_from_directory(
    cls,
    input_path: pathlib.Path,
    catalog: str,
    schema_name: str,
    schema_location: str,
    fail_on_missing_subfolder: bool = True,
    key: str | None = None
) -> tuple[list[Table], list[ValidationError | yaml.parser.ParserError]]
```

Read and instantiate all *.yaml files for the given path.

**Arguments**:

- `input_path` - Path to the directory containing the instance definitions as YAML files.
- `fail_on_missing_subfolder` - If False return a tuple with 2 empty
  lists. Otherwise raise a FileNotFoundError.
- `key` - The key to read from the dictionary.
- `catalog` - The catalog name to be used for the tables.
- `schema_name` - The schema name to be used for the tables.
- `schema_location` _str_ - The location of the schema. If specified the table is treated
  as "EXTERNAL TABLE" in Unity Catalog.
  

**Returns**:

  tuple(list[Instances], list[ValidationError]): Returns a tuple of
  the instantiated models and errors

<h4 id="table.Table.read_instance_from_file">read_instance_from_file</h4>

```python
@classmethod
def read_instance_from_file(
    cls,
    instance_path: pathlib.Path,
    catalog: str,
    schema_name: str,
    schema_location: str,
    key: str | None = None
) -> tuple[Table | None, list[ValidationError | yaml.parser.ParserError
                              | yaml.scanner.ScannerError]]
```

Read and instantiate a single YAML file for the given path.

**Arguments**:

- `instance_path` - The path to the file to instantiate.
- `key` - The key to read from the dictionary.
- `catalog` - The catalog name to be used for the table.
- `schema_name` - The schema name to be used for the table.
- `schema_location` _str_ - The location of the schema. If specified the table is treated
  as "EXTERNAL TABLE" in Unity Catalog.
  

**Returns**:

  Returns a tuple of the instantiated model and errors.

<h4 id="table.Table.metadata_to_instance">metadata_to_instance</h4>

```python
@classmethod
def metadata_to_instance(
        cls, data: dict) -> tuple[Table | None, list[ValidationError]]
```

Parses a Dictionary to an instance.

**Returns**:

  An instance and potentially a list of errors.

<h4 id="table.Table.name">name</h4>

```python
@property
def name() -> str
```

Returns the name of the table.

**Returns**:

- `str` - The name of the table.

<h4 id="table.Table.name">name</h4>

```python
@name.setter
def name(value: str)
```

Sets the name of the table and updates the identifier.

**Arguments**:

- `value(str)` - New name of the table.

<h4 id="table.Table.schema">schema</h4>

```python
@property
def schema() -> str
```

Returns the schema of the table.

**Returns**:

- `str` - The schema of the table.

<h4 id="table.Table.schema">schema</h4>

```python
@schema.setter
def schema(value: str)
```

Sets the schema of the table and updates the identifier.

**Arguments**:

- `value(str)` - New name of the schema.

<h4 id="table.Table.catalog">catalog</h4>

```python
@property
def catalog() -> str
```

Returns the catalog of the table.

**Returns**:

- `str` - The catalog of the table.

<h4 id="table.Table.catalog">catalog</h4>

```python
@catalog.setter
def catalog(value: str)
```

Sets the catalog of the table and updates the identifier.

**Arguments**:

- `value(str)` - New name of the catalog.

<h4 id="table.Table.primary_key">primary_key</h4>

```python
@property
def primary_key() -> list[Column]
```

Returns the primary key columns of the table.

**Returns**:

- `list(Column)` - The primary key columns of the table.

<h4 id="table.Table.escaped_identifier">escaped_identifier</h4>

```python
@property
def escaped_identifier() -> str
```

Returns the escaped identifier of the table.

**Returns**:

- `str` - The escaped identifier of the table.

<h4 id="table.Table.environment">environment</h4>

```python
@property
def environment() -> str
```

Derives the environment from the catalog name.

**Returns**:

- `Environment` - The Tables environment, derived from the catalog name.

<h4 id="table.Table.add_column">add_column</h4>

```python
def add_column(column: Column)
```

Adds a column to the table.

**Arguments**:

- `column` _Column_ - The column to be added.

<h4 id="table.Table.update_column">update_column</h4>

```python
def update_column(column: Column) -> None
```

Replaces a Column with a new Column object to update it.

**Arguments**:

- `column(Column)` - The new column object, to replace the old one.

<h4 id="table.Table.get_column_set_string">get_column_set_string</h4>

```python
def get_column_set_string() -> str
```

Returns a string of all columns in the table.

**Returns**:

- `str` - A string of all columns.

<h4 id="table.Table.generate_ddl">generate_ddl</h4>

```python
def generate_ddl(properties=None, options=None) -> str
```

Generates the DDL for the table.

**Arguments**:

- `properties` _dict, optional_ - The properties of the table.
- `options` _dict, optional_ - The options for the table.
  

**Returns**:

- `str` - The generated DDL for the table.

<h4 id="table.Table.generate_foreign_key_statements">generate_foreign_key_statements</h4>

```python
def generate_foreign_key_statements() -> str
```

Generates all ALTER TABLE statements based off of the Foreign Keys of the Table.

<h4 id="table.Table.set_location">set_location</h4>

```python
def set_location(location) -> Table
```

Sets the location of the table.

**Arguments**:

- `location` _str_ - The location to be set.
  

**Returns**:

- `Table` - The Table instance with the updated location.

<h4 id="table.Table.get_schema_string">get_schema_string</h4>

```python
def get_schema_string() -> str
```

Gets the schema in a comma seperated string.

**Example**:

  Col1 STRING, Col2 INT
  

**Returns**:

- `schema` - String representation of the Tables schema.

<h4 id="table.Table.get_column_by_name">get_column_by_name</h4>

```python
def get_column_by_name(column: str) -> Column
```

Gets a column by a name.

**Arguments**:

- `column` _str_ - Name of the Column.
  

**Raises**:

- `ValueError` - If the column is not part of the Table.
  

**Returns**:

- `Column` - The column object with the given name.

<h4 id="table.Table.remove_column">remove_column</h4>

```python
def remove_column(column: str | Column) -> None
```

Remove a column from the Table.

Args.
    column(str|Column): The column to be removed.

<h1 id="adapter">adapter</h1>

<h1 id="adapter.unity_catalog_adapter">adapter.unity_catalog_adapter</h1>

<h2 id="adapter.unity_catalog_adapter.UnityCatalogAdapter">UnityCatalogAdapter</h2>

```python
class UnityCatalogAdapter()
```

Acts as a translator between Unity Catalog metadata and WinDEF Models.

<h4 id="adapter.unity_catalog_adapter.UnityCatalogAdapter.__init__">__init__</h4>

```python
def __init__()
```

Initializes the UnityCatalogAdapter class.

<h4 id="adapter.unity_catalog_adapter.UnityCatalogAdapter.get_catalogs">get_catalogs</h4>

```python
def get_catalogs() -> list[Catalog]
```

Retrieve a list of catalogs with their associated metadata.

Returns: list[Catalog]: A list of `Catalog` objects.

<h4 id="adapter.unity_catalog_adapter.UnityCatalogAdapter.get_catalog_by_name">get_catalog_by_name</h4>

```python
def get_catalog_by_name(name: str) -> Catalog | None
```

Returns a Catalog by its name.

**Arguments**:

- `name` _str_ - The name of the Catalog.
  

**Returns**:

- `Catalog` - The Catalog with the specified name.

<h4 id="adapter.unity_catalog_adapter.UnityCatalogAdapter.get_catalog_schemas">get_catalog_schemas</h4>

```python
def get_catalog_schemas(catalog: str | Catalog) -> list[Schema]
```

Collects all schemas in a given catalog.

**Arguments**:

- `catalog` _str|Catalog_ - The catalog from which the schemas are to be collected.
  

**Returns**:

- `list[Schema]` - A list of `Schema` objects.

<h4 id="adapter.unity_catalog_adapter.UnityCatalogAdapter.get_schema_by_name">get_schema_by_name</h4>

```python
def get_schema_by_name(catalog: str | Catalog, name: str) -> Schema | None
```

Retrieve a schema by its name from a specified catalog.

**Arguments**:

- `catalog` _str | Catalog_ - The catalog from which to retrieve the schema.
  This can be either a string representing the catalog name or a
  `Catalog` object.
- `name` _str_ - The name of the schema to retrieve.
  

**Returns**:

  Schema | None: The `Schema` object if found, otherwise `None`.

<h4 id="adapter.unity_catalog_adapter.UnityCatalogAdapter.get_table_by_name">get_table_by_name</h4>

```python
def get_table_by_name(table_identifier: str) -> Table | None
```

Retrieve a table by it's name.

<h4 id="adapter.unity_catalog_adapter.UnityCatalogAdapter.add_tables_to_schema">add_tables_to_schema</h4>

```python
def add_tables_to_schema(catalog: str | Catalog,
                         schema: str | Schema) -> Schema
```

Add tables to a schema within a specified catalog.

This method retrieves all tables within the specified schema and catalog,
and adds them to the `Schema` object. The schema is updated with `Table`
objects containing details about each table.

**Arguments**:

- `catalog` _str | Catalog_ - The catalog containing the schema. This can be
  either a string representing the catalog name or a `Catalog` object.
- `schema` _str | Schema_ - The schema to which tables will be added. This
  can be either a string representing the schema name or a `Schema`
  object.
  

**Returns**:

- `Schema` - The updated `Schema` object with tables added.

<h4 id="adapter.unity_catalog_adapter.UnityCatalogAdapter.add_columns_to_table">add_columns_to_table</h4>

```python
def add_columns_to_table(table: Table) -> Table
```

Add columns to a table by retrieving column metadata from the information schema.

This method retrieves column details for the specified `table` from the
information schema and adds `Column` objects to the `Table`. It also identifies
primary key columns for the table.

**Arguments**:

- `table` _Table_ - The `Table` object to which columns will be added. The
  `Table` object must have its `identifier` attribute set.
  

**Returns**:

- `Table` - The updated `Table` object with columns added.

<h1 id="adapter.dataframe_adapter">adapter.dataframe_adapter</h1>

<h2 id="adapter.dataframe_adapter.DataFrameAdapter">DataFrameAdapter</h2>

```python
class DataFrameAdapter()
```

This adapter infers table metadata from a Dataframe.

It will read the column names and datatypes from the Spark dataframe.

<h4 id="adapter.dataframe_adapter.DataFrameAdapter.get_table">get_table</h4>

```python
def get_table(data_frame: DataFrame,
              table_identifier: str,
              location: str,
              primary_key: str | None = None,
              use_liquid_clustering: bool = True,
              partitioned_by: list[str] | None = None) -> Table
```

Read metadata from DataFrame and create table object.

**Arguments**:

- `data_frame` _DataFrame_ - DataFrame to read metadata from.
- `table_identifier` _str_ - Identifier of the table in the format 'catalog.schema.table'.
- `location` _str_ - Location on the physical storage.
- `primary_key` _str, optional_ - Primary key column of the table.
  Defaults to None.
- `partitioned_by` _list[str], optional_ - Partition columns of the
  table. Defaults to None.
- `use_liquid_clustering` _bool_ - Use liquid clustering. Defaults to
  true, requires Databricks Runtime 13.3 LTS or above.
  

**Raises**:

- `ValueError` - When primary_key or any partitioned_by column is not in
  the columns of the dataframe.
  

**Returns**:

- `Table` - A Table object representing the table.

<h1 id="data_contract">data_contract</h1>

<h1 id="data_contract.data_contract">data_contract.data_contract</h1>

<h2 id="data_contract.data_contract.DatacontractCatalogueRecordSchema">DatacontractCatalogueRecordSchema</h2>

```python
class DatacontractCatalogueRecordSchema(BaseModel)
```

A class that represents a catalogue record with metadata.

<h2 id="data_contract.data_contract.DatacontractDatasetSchema">DatacontractDatasetSchema</h2>

```python
class DatacontractDatasetSchema(BaseModel)
```

A class that represents a dataset with metadata.

<h4 id="data_contract.data_contract.DatacontractDatasetSchema.validate_data_product_type">validate_data_product_type</h4>

```python
@field_validator("data_product_type")
@classmethod
def validate_data_product_type(cls, value)
```

Validate that the data product type is either 'Source', 'Core', 'Primary' or 'Secondary'.

<h4 id="data_contract.data_contract.DatacontractDatasetSchema.validate_language">validate_language</h4>

```python
@field_validator("language")
@classmethod
def validate_language(cls, value)
```

Validate that the language is a 3-letter ISO 639-2 code.

<h4 id="data_contract.data_contract.DatacontractDatasetSchema.validate_frequency">validate_frequency</h4>

```python
@field_validator("frequency")
@classmethod
def validate_frequency(cls, value)
```

Validate that the frequency is one of the valid options.

<h4 id="data_contract.data_contract.DatacontractDatasetSchema.validate_version">validate_version</h4>

```python
@field_validator("version")
@classmethod
def validate_version(cls, value)
```

Validate that the version follows semantic versioning format.

<h2 id="data_contract.data_contract.DatacontractSchema">DatacontractSchema</h2>

```python
class DatacontractSchema(BaseModel)
```

Data Contract Model.

<h4 id="data_contract.data_contract.DatacontractSchema.metadata_to_instance">metadata_to_instance</h4>

```python
@classmethod
def metadata_to_instance(
        cls,
        data: dict) -> tuple[DatacontractSchema | None, list[ValidationError]]
```

Parses a Dictionary to an instance.

**Returns**:

  An instance and potentially a list of errors.

<h4 id="data_contract.data_contract.DatacontractSchema.read_instance_from_file">read_instance_from_file</h4>

```python
@classmethod
def read_instance_from_file(
    cls, instance_path: pathlib.Path
) -> tuple[
        DatacontractSchema | None,
        list[ValidationError | yaml.parser.ParserError
             | yaml.scanner.ScannerError],
]
```

Read and instantiate a single YAML file for the given path.

**Arguments**:

- `instance_path` - The path to the file to instantiate.
  

**Returns**:

  Returns a tuple of the instantiated model and errors.

<h1 id="data_contract.dataset">data_contract.dataset</h1>

<h2 id="data_contract.dataset.ValidationSchema">ValidationSchema</h2>

```python
class ValidationSchema(BaseModel)
```

A class that represents a data validation rule.

<h2 id="data_contract.dataset.FieldSchema">FieldSchema</h2>

```python
class FieldSchema(BaseModel)
```

A class that represents a field in a dataset schema.

<h2 id="data_contract.dataset.DatasetSchema">DatasetSchema</h2>

```python
class DatasetSchema(BaseModel)
```

A class that represents a dataset schema with metadata.

<h4 id="data_contract.dataset.DatasetSchema.validate_format">validate_format</h4>

```python
@field_validator("format")
@classmethod
def validate_format(cls, value)
```

Validate that the format is one of the valid options.

<h4 id="data_contract.dataset.DatasetSchema.metadata_to_instance">metadata_to_instance</h4>

```python
@classmethod
def metadata_to_instance(
        cls, data: dict) -> tuple[DatasetSchema | None, list[ValidationError]]
```

Parses a Dictionary to an instance.

**Returns**:

  An instance and potentially a list of errors.

<h4 id="data_contract.dataset.DatasetSchema.read_instance_from_file">read_instance_from_file</h4>

```python
@classmethod
def read_instance_from_file(
    cls, instance_path: pathlib.Path
) -> tuple[DatasetSchema | None, list[ValidationError | yaml.parser.ParserError
                                      | yaml.scanner.ScannerError]]
```

Read and instantiate a single YAML file for the given path.

**Arguments**:

- `instance_path` - The path to the file to instantiate.
  

**Returns**:

  Returns a tuple of the instantiated model and errors.

<h4 id="data_contract.dataset.DatasetSchema.get_table_docs">get_table_docs</h4>

```python
def get_table_docs() -> str
```

Generates a Markdown document describing the dataset.

**Returns**:

- `str` - Markdown document describing the dataset.

