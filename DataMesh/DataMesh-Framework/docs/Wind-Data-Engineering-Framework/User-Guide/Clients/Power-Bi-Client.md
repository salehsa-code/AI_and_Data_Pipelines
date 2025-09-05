# Power Bi Client

## Introduction

The Power Bi Client is a client that allows you to connect to a
Power Bi Service tenant and perform operations on it. A common
use case is to refresh a dataset.

## How To: Refresh a Dataset

The following example shows how to refresh a dataset.

```python
from windef.powerbi_client import PowerBiClient

client_id = "Service Principal Application Id"
client_secret = "DON'T HARDCODE THIS!"  # take e.g. from dbutils key vault integration
client = PowerBiClient(client_id, client_secret)

client.trigger_and_wait_for_refresh("Workspace Name", "Dataset Name")
```

The above describes the most basic usage of the client. The `trigger_and_wait_for_refresh`
method will trigger a refresh of the dataset and wait for it to finish. The
time it waits increases after each check until it reaches the maximum limit
set by the `max_refresh_check_time` parameter. The default is 30 seconds. The
method will return a string with the refresh status.

Alternatively, you can trigger a refresh with the `trigger_refresh` method
directly. This will trigger the refresh and immediately return the
refresh endpoint as string.

Mind, that:

- Datasets on a shared capacity can only be refreshed a maximum of eight times
  per day, including refreshes executed by using scheduled refresh. The API
  will then return a HTTP 429 response and the client will
  retry and wait for up to 3 minutes.
  > In reality I could not confirm the limit of 8 refreshes per day, but
  > a higher limit seems to be in place.
- Refreshes on the premium capacity might be throttled, depending on the
  capacity settings.

### Partial Refresh

By default, the client will trigger a full refresh of the dataset.
But you can specify a Body to configure a partial refresh.

```python
# ... same as above
body = {
    "type": "full",
    "commitMode": "transactional",
    "objects": [
        {
        "table": "Customer",
        "partition": "Robert"
        }
    ],
    "applyRefreshPolicy": "false"
}
client.trigger_and_wait_for_refresh("Workspace Name", "Dataset Name", body)
```

Mind, that only datasets on a Premium Capacity support partial refresh.
See [the documentation](https://docs.microsoft.com/en-us/power-bi/refresh-partial-dataset)
for an extended description of options and limitations.
