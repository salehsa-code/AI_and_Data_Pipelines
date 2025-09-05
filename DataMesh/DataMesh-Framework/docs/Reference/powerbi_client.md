# Table of Contents

* [exceptions](#exceptions)
* [powerbi\_client](#powerbi_client)

<h1 id="exceptions">exceptions</h1>

<h2 id="exceptions.RefreshAlreadyRunningException">RefreshAlreadyRunningException</h2>

```python
class RefreshAlreadyRunningException(Exception)
```

Raises an exception if a refresh is already running.

**Arguments**:

- `message` _str, optional_ - Error message. Defaults to "A refresh is already running.".

<h2 id="exceptions.WorkspaceNameError">WorkspaceNameError</h2>

```python
class WorkspaceNameError(Exception)
```

Raises an exception if a workspace name is referring to no workspace or multiple workspaces.

This exception is raised when a workspace name is invalid because it does not refer to any existing
workspace, or it refers to multiple workspaces.

<h2 id="exceptions.DatasetNameError">DatasetNameError</h2>

```python
class DatasetNameError(Exception)
```

Raises an exception if a dataset name is referring to no dataset or multiple datasets.

This exception is raised when a dataset name is invalid because it does not refer to any existing
dataset, or it refers to multiple datasets.

<h1 id="powerbi_client">powerbi_client</h1>

Module for interacting with PowerBI API.

This module provides a PowerBiClient class for connecting to and interacting
with the PowerBI API. It supports getting and refreshing access tokens,
making requests to the API, triggering dataset refreshes, and more.

<h2 id="powerbi_client.PowerBiClient">PowerBiClient</h2>

```python
class PowerBiClient()
```

A client for interacting with the PowerBI API.

**Arguments**:

- `client_id` _str_ - Client ID of the Azure AD Application.
- `client_secret` _str_ - Client Secret of the Azure AD Application.
- `tenant_id` _str, optional_ - Tenant ID of the Azure AD Application.
  Defaults to "f8be18a6-f648-4a47-be73-86d6c5c6604d".
- `_workspaces` _List[Dict], optional_ - A list of workspace dictionaries.
  Defaults to None.

<h4 id="powerbi_client.PowerBiClient.workspaces">workspaces</h4>

```python
@property
def workspaces()
```

Retrieves all workspaces.

**Returns**:

- `list` - List of all workspaces.

<h4 id="powerbi_client.PowerBiClient.trigger_refresh">trigger_refresh</h4>

```python
def trigger_refresh(workspace_name, dataset_name, body=None) -> str
```

Triggers a refresh of a dataset. In the body, you can specify the type of refresh you want to trigger.

API Limitations:
- For Shared capacities, a maximum of eight requests per day, including refreshes
executed by using scheduled refresh, can be initiated.
- For Shared capacities, only notifyOption can be specified in the request
body.
- Enhanced refresh is not supported for shared capacities.
- For Premium capacities, the maximum requests per day is only limited by the
available resources in the capacity. If available resources are overloaded,
refreshes are throttled until the load is reduced.
- The refresh will fail if throttling exceeds 1 hour.

For more details, refer to the official documentation
[here](https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/refresh-dataset#datasetrefreshobjects).

**Arguments**:

- `workspace_name` _str_ - The workspace name.
- `dataset_name` _str_ - The dataset name.
- `body` _str, optional_ - The body of the request. Defaults to None.
  

**Returns**:

- `str` - The refresh endpoint.
  

**Raises**:

- `RefreshAlreadyRunningException` - If a refresh is already in progress.

<h4 id="powerbi_client.PowerBiClient.trigger_and_wait_for_refresh">trigger_and_wait_for_refresh</h4>

```python
def trigger_and_wait_for_refresh(workspace_name: str,
                                 dataset_name: str,
                                 body: dict | None = None,
                                 max_refresh_check_time: int = 30)
```

Triggers a refresh of a dataset and waits for it to complete.

**Arguments**:

- `workspace_name` _str_ - The workspace name.
- `dataset_name` _str_ - The dataset name.
- `body` _Dict, optional_ - The body of the request. Defaults to None.
- `max_refresh_check_time` _int, optional_ - The maximum time to wait for refresh. Defaults to 30.
  

**Returns**:

- `str` - The refresh status.

