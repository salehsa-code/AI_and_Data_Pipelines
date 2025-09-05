# API Client

The API client module extends the `requests` library's `AuthBase` class to
create additional custom Auth classes that can support various ways of setting up authentication with an API endpoint.

:::mermaid
classDiagram
    class APIClient {
        base_url: str
        auth: AuthBase
        get(): APIResponse
        post(): APIResponse
        put(): APIResponse
        delete(): APIResponse
        patch(): APIResponse
    }
    class APIResponse {
      response: APIResponse
      to_dict()
    }
    class CustomAuth {
      __call__()
    }
    class `requests.auth.AuthBase` {
      <<Abstract>>
      __call__()
    }
    APIResponse <.. APIClient: return
    `requests.Session` -- APIClient: uses
    LoggingService -- APIClient: uses
    `requests.auth.AuthBase` -- APIClient: uses
    `requests.Response` -- APIResponse: uses
    `requests.auth.AuthBase` <|-- CustomAuth : implements
:::

## How To: Extend AuthBase Class

To create a new form of authentication, you can simply extend the request
library's `AuthBase` class. Please refere to
[this](https://requests.readthedocs.io/en/latest/user/authentication/#new-forms-of-authentication)
documentation for more details on the base class.

Your new implementation of the class must be derived from
`requests.auth.AuthBase` or one of the existing Auth classes and has to
implement the `__call__()` method.

```python
class MyAuth(requests.auth.AuthBase):
  def __call__(self, r):
    # Implement my authentication
    return r
```

Usually, the authentication module needs to add one or more fields to the request header. To do so, simply update the header in the `PreparedRequest` object `r`:

```python
  def __call__(self, r):
    # create auth_header
    # [...]
    r.headers.update(auth_header)
    return r
```
