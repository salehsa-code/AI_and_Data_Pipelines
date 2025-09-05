# Table of Contents

* [exceptions](#exceptions)
* [client](#client)
* [api\_response](#api_response)
* [auth](#auth)

<h1 id="exceptions">exceptions</h1>

<h2 id="exceptions.APIClientError">APIClientError</h2>

```python
class APIClientError(Exception)
```

Base class for API client exceptions.

<h2 id="exceptions.APIClientHTTPError">APIClientHTTPError</h2>

```python
class APIClientHTTPError(APIClientError)
```

Exception raised for HTTP errors.

<h2 id="exceptions.APIClientConnectionError">APIClientConnectionError</h2>

```python
class APIClientConnectionError(APIClientError)
```

Exception raised for connection errors.

<h2 id="exceptions.APIClientTimeoutError">APIClientTimeoutError</h2>

```python
class APIClientTimeoutError(APIClientError)
```

Exception raised for timeout errors.

<h1 id="client">client</h1>

<h2 id="client.APIClient">APIClient</h2>

```python
class APIClient()
```

A standardized client for the interaction with APIs.

<h4 id="client.APIClient.MAX_SLEEP_TIME">MAX_SLEEP_TIME</h4>

seconds

<h4 id="client.APIClient.get">get</h4>

```python
def get(endpoint: str, **kwargs: Any) -> APIResponse
```

Sends a GET request to the specified endpoint.

**Arguments**:

- `endpoint` - The endpoint to send the request to.
- `**kwargs` - Additional arguments to pass to the request.
  

**Returns**:

- `APIResponse` - The response from the API.

<h4 id="client.APIClient.post">post</h4>

```python
def post(endpoint: str, **kwargs: Any) -> APIResponse
```

Sends a POST request to the specified endpoint.

**Arguments**:

- `endpoint` - The endpoint to send the request to.
- `**kwargs` - Additional arguments to pass to the request.
  

**Returns**:

- `APIResponse` - The response from the API.

<h4 id="client.APIClient.put">put</h4>

```python
def put(endpoint: str, **kwargs: Any) -> APIResponse
```

Sends a PUT request to the specified endpoint.

**Arguments**:

- `endpoint` - The endpoint to send the request to.
- `**kwargs` - Additional arguments to pass to the request.
  

**Returns**:

- `APIResponse` - The response from the API.

<h4 id="client.APIClient.delete">delete</h4>

```python
def delete(endpoint: str, **kwargs: Any) -> APIResponse
```

Sends a DELETE request to the specified endpoint.

**Arguments**:

- `endpoint` - The endpoint to send the request to.
- `**kwargs` - Additional arguments to pass to the request.
  

**Returns**:

- `APIResponse` - The response from the API.

<h4 id="client.APIClient.patch">patch</h4>

```python
def patch(endpoint: str, **kwargs: Any) -> APIResponse
```

Sends a PATCH request to the specified endpoint.

**Arguments**:

- `endpoint` - The endpoint to send the request to.
- `**kwargs` - Additional arguments to pass to the request.
  

**Returns**:

- `APIResponse` - The response from the API.

<h4 id="client.APIClient.request">request</h4>

```python
def request(method: str, endpoint: str, **kwargs: Any) -> APIResponse
```

Sends a request to the specified endpoint with the specified method.

**Arguments**:

- `method` - The HTTP method to use for the request.
- `endpoint` - The endpoint to send the request to.
- `**kwargs` - Additional arguments to pass to the request.
  

**Returns**:

- `APIResponse` - The response from the API.

<h1 id="api_response">api_response</h1>

<h2 id="api_response.APIResponse">APIResponse</h2>

```python
class APIResponse()
```

An Abstracted response to implement parsing.

<h4 id="api_response.APIResponse.to_dict">to_dict</h4>

```python
def to_dict(key: str | None = None) -> dict[str, str]
```

Parses the values from the response into a dictionary.

**Arguments**:

- `key` _str_ - The key to return from the dict. Defaults to None.
  

**Returns**:

  The Response parsed to a dictionary and filtered by the key,
  if specified.
  

**Raises**:

  KeyError if the specified Key is not in the Response.

<h1 id="auth">auth</h1>

<h2 id="auth.AzureCredentialAuth">AzureCredentialAuth</h2>

```python
class AzureCredentialAuth(AuthBase)
```

This Auth can be used with requests and an Azure Credential.

<h4 id="auth.AzureCredentialAuth.__init__">__init__</h4>

```python
def __init__(scope: str,
             credential: TokenCredential | ClientSecretCredential
             | None = None,
             client_id: str | None = None,
             client_secret: str | None = None,
             tenant_id: str | None = None)
```

Initializes the AzureCredentialAuth with an Azure credential.

The client can either be initialized with a TokenCredential object or with the client_id, client_secret, and tenant_id via an ClientSecretCredential.

**Arguments**:

- `scope` - The scope for the token. E.g., the client ID of the Azure AD application.
- `credential` - The Azure credential object.
- `client_id` - The client ID for the Azure AD application.
- `client_secret` - The client secret for the Azure AD application.
- `tenant_id` - The tenant ID for the Azure AD application.

<h4 id="auth.AzureCredentialAuth.token">token</h4>

```python
@property
def token()
```

Get a valid token using the TokenCredential.

<h4 id="auth.AzureCredentialAuth.__call__">__call__</h4>

```python
def __call__(r: PreparedRequest) -> PreparedRequest
```

Appends an Authorization header to the request using the provided Azure credential.

**Arguments**:

- `r` _PreparedRequest_ - The request that needs to be sent.
  

**Returns**:

- `PreparedRequest` - The same request object but with an added Authorization header.

<h2 id="auth.SecretScopeAuth">SecretScopeAuth</h2>

```python
class SecretScopeAuth(AuthBase)
```

This Auth pulls Secrets from a Secret Scope.

<h4 id="auth.SecretScopeAuth.__init__">__init__</h4>

```python
def __init__(header_template: dict[str, str], secret_scope: str)
```

Initializes the SecretScopeAuth with a header template, secret scope, and secret key.

**Arguments**:

- `header_template` _dict[str, str]_ - The template for the header that will use the secret.
  secret names are defined as placeholders in curly braces.
- `secret_scope` _str_ - The secret scope from where the secrets will be retrieved.

<h4 id="auth.SecretScopeAuth.__call__">__call__</h4>

```python
def __call__(r: PreparedRequest) -> PreparedRequest
```

The header is constructed using the template and the secret retrieved from the secret scope.

**Arguments**:

- `r` _PreparedRequest_ - The request that needs to be sent.
  

**Returns**:

- `PreparedRequest` - The same request object, but with an added header. The header
  is constructed using the template and the secret retrieved from
  the secret scope.
  

**Example**:

```python
header_template = {
    "jfrog-user-key": "jfrog-user",
    "jfrog-password-key": "jfrog-secret",
}
auth = SecretScopeAuth(header_template, "my_secret_scope")
# given, that 'jfrog-user' and 'jfrog-secret' are secrets in 'my_secret_scope'
```

<h2 id="auth.ChainedAuth">ChainedAuth</h2>

```python
class ChainedAuth(AuthBase)
```

This Auth can be used to chain multiple Auths.

<h4 id="auth.ChainedAuth.__init__">__init__</h4>

```python
def __init__(*args)
```

Initializes the ChainedAuth.

**Arguments**:

- `*args` - One or more Auth objects that are chanined to
  construct the auth header.
    ```

<h4 id="auth.ChainedAuth.__call__">__call__</h4>

```python
def __call__(r: PreparedRequest) -> PreparedRequest
```

The header is constructed using the template and the secret retrieved from the secret scope.

**Arguments**:

- `r` _PreparedRequest_ - The request that needs to be sent.
  

**Returns**:

- `PreparedRequest` - The same request object, but with an added header. The header
  is constructed using the template and the secret retrieved from
  the secret scope.
  

**Example**:

```python
auth_1 = SecretScopeAuth({"secret": "key"}, "my_secret_scope")
auth_2 = SecretScopeAuth({"secret": "key"}, "my_other_secret_scope")
chained_auth = ChainedAuth(auth_1, auth_2)
```

<h2 id="auth.EnvVariableAuth">EnvVariableAuth</h2>

```python
class EnvVariableAuth(AuthBase)
```

This Auth can be used to create an auth header from environment variables.

<h4 id="auth.EnvVariableAuth.__init__">__init__</h4>

```python
def __init__(header_template: dict[str, str])
```

Initializes the EnvVariableAuth with a header template.

**Arguments**:

- `header_template` _dict[str,str]_ - The template for the header that will use the envrionment variables.
  variable names are defined as placeholders.

<h4 id="auth.EnvVariableAuth.__call__">__call__</h4>

```python
def __call__(r: PreparedRequest) -> PreparedRequest
```

The header is constructed using the template and the secret retrieved from the secret scope.

**Arguments**:

- `r` _PreparedRequest_ - The request that needs to be sent.
  

**Returns**:

- `PreparedRequest` - The same request object, but with an added header. The header
  is constructed using the template and the secret retrieved from
  environment variables.
  

**Example**:

```python
header_template = {
    "user": "USER_NAME",
    "password": "USER_SECRET",
}
auth = EnvVariableAuth(header_template)
# given, that "USER_NAME" and "USER_SECRET" are envrionment variables
```

