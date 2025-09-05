# Table of Contents

* [alation\_client](#alation_client)

<h1 id="alation_client">alation_client</h1>

This module provides a client to interface with the Alation service.

The AlationClient class allows for creating and managing resources in Alation, including
creating tokens, creating and managing data sources, uploading various types of metadata,
and managing data lineage.

<h2 id="alation_client.APIError">APIError</h2>

```python
class APIError(Exception)
```

Class to represent an API error.

<h2 id="alation_client.AlationClient">AlationClient</h2>

```python
class AlationClient()
```

Alation Client class to interface with the Alation service.

**Arguments**:

- `username` _str_ - The Alation username.
- `password` _str_ - The password for the Alation user.
- `env` _str_ - The environment (e.g., 'tst' or 'prd').
- `adc_base_url` _str_ - The base URL for the Alation Data Catalog.
- `user_id` _int_ - The user ID for the Alation user.
- `refresh_token` _str_ - The refresh token for the Alation API.
- `api_access_token` _str_ - The access token for the Alation API.
- `data_source_id` _int_ - The ID of the data source in Alation.

<h4 id="alation_client.AlationClient.__init__">__init__</h4>

```python
def __init__(username: str, password: str, env: str)
```

Initializes the client.

**Arguments**:

- `username` _str_ - The Alation user.
- `password` _str_ - The Alation password for the user.
- `env` _str_ - The environment (prd/tst).

<h4 id="alation_client.AlationClient.get_endpoint">get_endpoint</h4>

```python
def get_endpoint(endpoint: str) -> str
```

Returns the base alation url joined with the provided endpoint.

**Arguments**:

- `endpoint` _str_ - The endpoint path.
  

**Returns**:

- `str` - The joined URL.

<h4 id="alation_client.AlationClient.create_virtual_datasource">create_virtual_datasource</h4>

```python
def create_virtual_datasource(title: str, description: str, is_private: bool,
                              is_virtual: bool, dbtype: str)
```

Creates a virtual data source in Alation.

**Arguments**:

- `title` _str_ - The name of the data source.
- `description` _str_ - Description of the data source.
- `is_private` _bool_ - Whether the data source should be private.
- `is_virtual` _bool_ - Whether the data source is virtual.
- `dbtype` _str_ - The type of the data source (mssql, mysql, generic_nosql, etc.).
  

**Returns**:

- `requests.Response` - The response from the POST request.

<h4 id="alation_client.AlationClient.get_datasource">get_datasource</h4>

```python
def get_datasource(title: str) -> bool
```

Checks if a virtual data source is already created in Alation.

**Arguments**:

- `title` _str_ - The name of the data source.
  

**Returns**:

- `bool` - True if the data source already exists, False otherwise.
  

**Raises**:

- `ValueError` - If the title of the data source does not start with 'Wind.VAP2'. This
  is a security measure to prevent accidental deletion of foreign data sources.

<h4 id="alation_client.AlationClient.upload_technical_metadata">upload_technical_metadata</h4>

```python
def upload_technical_metadata(data: dict[str, Any])
```

Uploads technical metadata to Alation.

**Arguments**:

- `data` _dict[str, Any]_ - A JSON string containing metadata.
  

**Returns**:

- `requests.Response` - The response from the POST request.

<h4 id="alation_client.AlationClient.upload_logical_metadata">upload_logical_metadata</h4>

```python
def upload_logical_metadata(data: str)
```

Uploads logical metadata to Alation.

**Arguments**:

- `data` _str_ - A JSON string containing metadata.
  

**Returns**:

- `requests.Response` - The response from the POST request.

<h4 id="alation_client.AlationClient.upload_schema">upload_schema</h4>

```python
def upload_schema(data: str | dict | Schema)
```

Uploads a schema to the associated data source.

Define either the data as string or dict OR the schema.

**Arguments**:

- `data` _str|dict|Schema_ - The schema data to be uploaded.
  

**Returns**:

- `requests.Response` - The response from the POST request.
  

**Raises**:

- `ValueError` - If the Input Arguments are invalid.

<h4 id="alation_client.AlationClient.upload_table">upload_table</h4>

```python
def upload_table(data: str | dict | Table)
```

Uploads a table to the associated data source.

Define either the data as string or dict OR the table.

**Arguments**:

- `data` _str|dict|Table_ - The table data to be uploaded.
  

**Returns**:

- `requests.Response` - The response from the POST request.
  

**Raises**:

- `ValueError` - If the Input Arguments are invalid.

<h4 id="alation_client.AlationClient.upload_columns">upload_columns</h4>

```python
def upload_columns(data: str | dict | Table)
```

Uploads columns to the associated data source.

Define either the data as string or dict OR the table.

**Arguments**:

- `data` _str|dict|Table_ - The column data to be uploaded.
  

**Returns**:

- `requests.Response` - The response from the POST request.
  

**Raises**:

- `ValueError` - If the Input Arguments are invalid.

<h4 id="alation_client.AlationClient.upload_data_contract">upload_data_contract</h4>

```python
def upload_data_contract(datasource_title: str, path: str)
```

Upload the Metadata for a DataContract.

**Arguments**:

- `datasource_title` _str_ - The name of the Data Source in Alation.
- `path` _str_ - Path to the data contract to upload.
  

**Raises**:

- `ValueError` - If there are errors while reading the data contract.
- `ValueError` - If no schema could be instantiated from the data contract.

<h4 id="alation_client.AlationClient.upload_schema_from_unity_catalog">upload_schema_from_unity_catalog</h4>

```python
def upload_schema_from_unity_catalog(datasource_title: str, catalog_name: str,
                                     schema_name: str)
```

Upload the Metadata for a Schema in Unity Catalog.

**Arguments**:

- `datasource_title` _str_ - The name of the Data Source in Alation.
- `catalog_name` _str_ - The name of the Catalog in Unity.
- `schema_name` _str_ - The name of the Schema to upload.

<h4 id="alation_client.AlationClient.upload_data_lineage">upload_data_lineage</h4>

```python
def upload_data_lineage(data: str) -> None
```

Uploads data lineage data to Alation.

**Arguments**:

- `data` _str_ - A JSON string containing lineage data.

<h4 id="alation_client.AlationClient.list_objects_in_datasource">list_objects_in_datasource</h4>

```python
def list_objects_in_datasource(limit)
```

Lists objects in the associated data source.

**Arguments**:

- `limit` _int_ - The maximum number of objects to be returned.
  

**Returns**:

- `list` - The list of objects in the data source.

<h4 id="alation_client.AlationClient.get_lineage_data_to_delete">get_lineage_data_to_delete</h4>

```python
def get_lineage_data_to_delete(objects)
```

Gets lineage data to be deleted for a list of objects.

**Arguments**:

- `objects` _list_ - The list of objects for which the lineage data is to be deleted.
  

**Returns**:

- `list` - The list of lineage data to be deleted.

<h4 id="alation_client.AlationClient.remove_lineage_data">remove_lineage_data</h4>

```python
def remove_lineage_data(limit)
```

Removes lineage data for a certain number of objects in the associated data source.

**Arguments**:

- `limit` _int_ - The maximum number of objects for which the lineage data is to be removed.
  

**Returns**:

- `requests.Response` - The response from the DELETE request.

<h4 id="alation_client.AlationClient.remove_metadata">remove_metadata</h4>

```python
def remove_metadata()
```

Removes all objects from the associated data source's metadata.

**Returns**:

- `requests.Response` - The response from the POST request.

<h4 id="alation_client.AlationClient.remove_all_data">remove_all_data</h4>

```python
def remove_all_data(limit)
```

Removes all data for a certain number of objects in the associated data source.

**Arguments**:

- `limit` _int_ - The maximum number of objects for which the data is to be removed.
  

**Returns**:

- `requests.Response` - The response from the POST request to remove metadata.

<h4 id="alation_client.AlationClient.delete_datasource">delete_datasource</h4>

```python
def delete_datasource()
```

Deletes the associated data source.

**Returns**:

- `requests.Response` - The response from the DELETE request.

