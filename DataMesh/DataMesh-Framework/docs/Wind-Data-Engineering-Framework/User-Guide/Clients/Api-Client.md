# Api Client

## Overview

The API Client module is designed to aid developers in integrating API use-cases
rapidly. The client supports:

- Easy handling of Authorization, e.g., via AzureTokenCredential, Environment
  Variables, or SecretScope values.
- Setup of a session that handles default headers and authentication.
- All regular HTTP request methods: GET, POST, DELETE, PATCH, PUT.

This is the regular flow using this client:

:::mermaid
graph LR
    A[Import requirements]
    B[Initialize Auths]
    C[Initialize APIClient]
    D[Make requests]
    E[Parse Response]

    A --> B --> C--> D--> E
:::

Please check [the Reference](/docs/Reference/api_client.md) for a full overview
on all methods implemented by the classes in the `api_client` module.

The list of available Auth methods includes:

- Auth classes defined by the [requests
  library](https://requests.readthedocs.io/en/latest/user/authentication/),
  e.g., HTTPBasicAuth (Username and Password).
- *AzureCredentialAuth*: Authentication using an Entra ID Token for OAuth2 flows.
- *SecretScopeAuth*: Include secrets from a secret scope.
- *EnvVariableAuth*: Include secrets from environment variables.
- *ChainedAuth*: Combine different Auths.

> If your usecase is not covered by these Auths, it is easy to extend them. Please approach us!

## How To: Initialize the Api Client and make a request

Typically the API to consume is not publically available, thus requiring
the need to define the authorization first.

```python
from requests.auth import HTTPBasicAuth
from windef.api_client import APIClient

auth = HTTPBasicAuth("user", "password")

client = APIClient("https://www.example.com", auth)
client.get("/interesting-endpoint", params={"query":"good_stuff"})
```

## How To: Make a request using an Entra Id Token

When communicating with Microsoft APIs, authorization is often possible with an
Entra ID Token. Here is an example listing the resources within a resource
group.

```bash
# manually login to az cli
$ az login --use-device-code
```

```python
from azure.identity import DefaultAzureCredential
from windef.api_client import APIClient, AzureCredentialAuth

credential = DefaultAzureCredential()  # authenticated via az cli
scope = "https://management.azure.com/.default"
auth = AzureCredentialAuth(credential, scope)
client = APIClient("https://management.azure.com/", auth)
subscriptionId = "your-subscription-id"
resourceGroupName = "your-resource-group"
response = client.get(
    f"subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}",
    params={"api-version": "2021-04-01"},
)
```

The response returns an `APIResponse` object. This is a wrapper around the
regular `Response` object created by the `requests` library. It offers methods
to parse the response into different formats. E.g., to a Dictionary:

```python
# code from above
response.to_dict()
```

> Currently this Class only supports a `to_dict` method, but it would be easy to
> extend for other formats, e.g., XML.

## How To: Make a request using variables from a Secret Scope

Secrets within Databricks are typically stored in secret scopes. To use values
from a secret scope for your request, you have to create a `header_template` and
specify the `secret_scope` that contains the secrets.

```python
from windef.api_client import SecretScopeAuth
header_template = {
    "user-key": "jfrog-user",
    "password-key": "jfrog-secret",
}
auth = SecretScopeAuth(header_template, "my_secret_scope")
# Given that 'jfrog-user' and 'jfrog-secret' are secrets in 'my_secret_scope'
# this will result in this header:
{
    "user-key": "<Value for 'jfrog-user' from 'my_secret_scope'>"
    "password-key": "<Value for 'jfrog-secret' from 'my_secret_scope'>"
}
```

> How the headers are implemented is transparent to you as a user and is
> explained here for clarity.

## How To: Make a request using multiple Auths

Many APIs will require some static part of authentication (e.g. an API Token)
and some dynamic authentication (e.g. an OAuth Token). For this Usecase the
APIClient supports ChainedAuth.

This is an example querying data from a CAPIM Source (MO4):

```python
from windef.api_client import APIClient, AzureCredentialAuth, ChainedAuth, SecretScopeAuth
from azure.identity import ClientSecretCredential

# Setup variables for OAuth authentication
tenant_id = "f8be18a6-f648-4a47-be73-86d6c5c6604d"
mo4_app_id = dbutils.secrets.get("vap2-winddata-atm-kv","MO4-app-id")
mo4_app_secret = dbutils.secrets.get("vap2-winddata-atm-kv","MO4-app-secret")

# Setup OAuth via Azure Entra ID
azure_credential = ClientSecretCredential(tenant_id, mo4_app_id, mo4_app_secret)
azure_auth = AzureCredentialAuth(azure_credential, "3042ad64-5cc1-413c-ad13-3ad450cbc999/.default")

# Setup static Authentication variables via secret scope
secret_scope_auth = SecretScopeAuth(header_template={
      "X-API-Key": "MO4-api-key",
      "Ocp-Apim-Subscription-Key": "MO4-subscription-key",
    }, secret_scope="vap2-winddata-atm-kv")

# Initialize the client
client = APIClient(
    "https://sys.api.vattenfall.com/internalapi/mo4/",
    ChainedAuth(azure_auth, secret_scope_auth),
)

# The header will look like this:
# {
#   "Authorization": "Bearer <Entra ID Token>",
#   "X-API-Key": "<API Key>",
#   "Ocp-Apim-Subscription-Key": "<Subscription Key>",
# }

# Use the client
response = client.get("vessels")
vessels = response.to_dict()  # store the return value as dictionary
```

## Error Handling

This module includes error handling for different types of errors:

- `HTTPError` - This error is raised when an HTTP request returns an
  unsuccessful status code. The error message will include details about the
  request and the status code.
- `ConnectionError` - This error is raised when there is a network problem, like
  a DNS resolution failure, refused connection, etc.
- `Timeout` - This error is raised when a request times out. These errors are
handled in the `_make_request` method, and the error message will be logged
before the error is raised. If you're using this module in your application, you
should be prepared to handle these errors as appropriate

```python
try:
    client = APIClient("https://www.example.com", auth)
    client.get("/interesting-endpoint", params={"query":"good_stuff"})
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
except requests.exceptions.ConnectionError as err:
    print(f"Error connecting: {err}")
except requests.exceptions.Timeout as err:
    print(f"Timeout error: {err}")
```

For errors at the application level, like passing an invalid argument to a
function or a missing environment variable, Python's built-in exception handling
will take care of it. For example, if you're using the EnvVariableAuth class and
the specified environment variable does not exist, Python will raise a KeyError.

```python
try:
    auth = EnvVariableAuth({"user": "NON_EXISTENT_ENV_VAR"})
except KeyError as err:
    print(f"Environment variable not found: {err}")
```
