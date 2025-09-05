# Table of Contents

* [log\_analytics\_handler](#log_analytics_handler)
* [logging\_service](#logging_service)

<h1 id="log_analytics_handler">log_analytics_handler</h1>

This module provides a custom logging handler for Azure Log Analytics.

The LogAnalyticsHandler class extends the standard Python logging.Handler class
and sends log messages to Azure Log Analytics Workspace. It parses the log messages
according to the provided column and key-value split characters and converts them
into a dictionary that is compliant with the Azure Log Analytics API.

**Example**:

```python
import logging
from windef.logging import LogAnalyticsHandler

workspace_id = "your_workspace_id"
shared_key = "your_shared_key"
log_type = "your_log_type"

logger = logging.getLogger("azure_log_analytics_logger")
logger.setLevel(logging.INFO)

handler = LogAnalyticsHandler(workspace_id, shared_key, log_type)
logger.addHandler(handler)

logger.info("key1:value1 | key2:value2 | key3:value3")
```

<h2 id="log_analytics_handler.LogAnalyticsHandler">LogAnalyticsHandler</h2>

```python
class LogAnalyticsHandler(logging.Handler)
```

A custom logging handler for Azure Log Analytics.

The handler will by default always send the timestamp and loglevel of the log message.

**Attributes**:

- `METHOD` _str_ - The HTTP method for the requests.
- `RESOURCE` _str_ - The resource path for the requests.
- `CONTENT_TYPE` _str_ - The content type for the requests.

<h4 id="log_analytics_handler.LogAnalyticsHandler.__init__">__init__</h4>

```python
def __init__(workspace_id: str,
             shared_key: str,
             log_type: str,
             column_split_char: str = "|",
             key_value_split_char: str = ":",
             test_connectivity: bool = True)
```

Initializes a new instance of the LogAnalyticsHandler class.

**Arguments**:

- `workspace_id` _str_ - The workspace ID for Azure Log Analytics.
- `shared_key` _str_ - The shared key for Azure Log Analytics.
- `log_type` _str_ - The log type for Azure Log Analytics.
- `column_split_char` _str, optional_ - The character used to split columns in the log message. Defaults to "|".
- `key_value_split_char` _str, optional_ - The character used to split keys and values in the log message.
  Defaults to ":".
- `test_connectivity` _bool, optional_ - Whether to test connectivity to Azure Log Analytics when initializing
  the handler. Defaults to True.

<h4 id="log_analytics_handler.LogAnalyticsHandler.test_connectivity">test_connectivity</h4>

```python
def test_connectivity()
```

Checks the connectivity to the Log Analytics workspace without sending a log.

**Raises**:

- `ValueError` - If the connection to Azure Log Analytics fails.

<h4 id="log_analytics_handler.LogAnalyticsHandler.__eq__">__eq__</h4>

```python
def __eq__(other)
```

Checks if two LogAnalyticsHandler instances are equal.

Instances are considered equal if they have the same workspace_id, shared_key, and log_type.
This will prevent the same handler from being added multiple times to a single logger.

**Arguments**:

- `other` _LogAnalyticsHandler_ - The other LogAnalyticsHandler instance to compare with.
  

**Returns**:

- `bool` - True if instances are equal, False otherwise.

<h4 id="log_analytics_handler.LogAnalyticsHandler.__hash__">__hash__</h4>

```python
def __hash__()
```

Generates a unique hash value for the object.

This method overrides the built-in `__hash__` method to generate a unique hash value for the object,
which is particularly useful for using the object in sets or as keys in dictionaries.

The hash value is computed based on the 'workspace_id', 'shared_key', and 'log_type' attributes of the object.

<h4 id="log_analytics_handler.LogAnalyticsHandler.emit">emit</h4>

```python
def emit(record: logging.LogRecord)
```

Sends the log message to Azure Log Analytics.

**Arguments**:

- `record` _logging.LogRecord_ - The record instance with the log message.
  

**Raises**:

- `ValueError` - If record.msg is not a string, or if failed to send log to Azure Log Analytics.
  

**Notes**:

  This method uses the following methods:
  - _parse_string_to_dict to convert the log message to a dictionary.
  - _make_message_compliant to make the log message compliant.
  - _build_signature to build the signature for the request.
  - _get_url to get the URL of the Azure Log Analytics workspace.

<h4 id="log_analytics_handler.LogAnalyticsHandler.escape_string">escape_string</h4>

```python
def escape_string(input_string: str) -> str
```

Escapes special characters in the input string.

**Arguments**:

- `input_string` _str_ - The string to escape.
  

**Returns**:

- `str` - The escaped string.

<h1 id="logging_service">logging_service</h1>

This module provides a standard logging service for the WinDEF package.

**Example**:

  Variables are read from the environment variables:
  
```python
import os
os.environ['LOG_ANALYTICS_WORKSPACE_ID'] = 'your_workspace_id'
os.environ['LOG_ANALYTICS_WORKSPACE_SHARED_KEY'] = 'your_shared_key'
os.environ['LOG_TYPE'] = 'your_log_type'
os.environ['WINDEF_LOG_TO_AZURE'] = 'True'
my_logger = LoggingService().get_logger()
my_logger.info('Column1:Value1 | Column2:Value2')
```
  
  Alternatively, they are set explicitly:
  
```python
my_logger = LoggingService(
    logging.DEBUG,
    'your_workspace_id',
    'your_shared_key',
    'your_log_type'
).get_logger()
my_logger.debug('Column1:Value1 | Column2:Value2')
```

<h2 id="logging_service.LoggingService">LoggingService</h2>

```python
class LoggingService()
```

The LoggingService class serves as a standard logging service for the WinDEF package.

This class encapsulates the built-in Python logging module, providing a standardized logger
instance with pre-configured settings for formatting and handling. This ensures consistent
logging practices throughout the WinDEF package.

**Attributes**:

- `logger` _logging.Logger_ - An instance of a logger with predefined settings.

<h4 id="logging_service.LoggingService.__init__">__init__</h4>

```python
def __init__(logger_name: str = __name__,
             log_level: int = logging.INFO,
             workspace_id: str | None = None,
             shared_key: str | None = None,
             log_type: str | None = None,
             column_split_char: str = "|",
             key_value_split_char: str = ":",
             test_connectivity: bool = True,
             log_to_azure: bool | None = None,
             log_to_console: bool | None = True)
```

Initializes a new instance of the LoggingService class.

**Arguments**:

- `logger_name` _str, optional_ - The name of the logger. Defaults to __name__.
- `log_level` _int, optional_ - The level of the logger. Defaults to logging.INFO.
- `workspace_id` _str, optional_ - The workspace ID for Azure Log Analytics. Defaults to None.
- `shared_key` _str, optional_ - The shared key for Azure Log Analytics. Defaults to None.
- `log_type` _str, optional_ - The log type for Azure Log Analytics. Defaults to None.
- `column_split_char` _str, optional_ - The character used to split columns in the log message. Defaults to "|".
- `key_value_split_char` _str, optional_ - The character used to split keys and values in the log message.
  Defaults to ":".
- `test_connectivity` _bool, optional_ - Whether to test connectivity to Azure Log Analytics when initializing
  the handler. Defaults to True.
- `log_to_azure` _bool, optional_ - Whether to log to Azure Log Analytics. Defaults to True.
- `log_to_console` _bool, optional_ - Whether to log to console. Defaults to True.

<h4 id="logging_service.LoggingService.get_handler_by_class_name">get_handler_by_class_name</h4>

```python
@staticmethod
def get_handler_by_class_name(
        logger: logging.Logger,
        handler_class_name: str) -> logging.Handler | None
```

Returns the handler with the specified class name.

**Arguments**:

- `logger` _logging.Logger_ - The logger instance to search.
- `handler_class_name` _str_ - The name of the handler class to search for.
  

**Returns**:

  logging.Handler | None: The handler instance if found, otherwise None.

<h4 id="logging_service.LoggingService.get_logger">get_logger</h4>

```python
def get_logger() -> logging.Logger
```

Returns the logger instance for use.

**Returns**:

- `logging.Logger` - The logger instance.

<h4 id="logging_service.LoggingService.table_log_decorator">table_log_decorator</h4>

```python
@staticmethod
def table_log_decorator(operation: str)
```

Creates a decorator that logs the start, failure (if any), and completion of a table operation.

The created decorator wraps a function that performs an operation on a table. The decorator logs
the start of the operation, calls the original function, logs if there was an exception, and logs
the completion of the operation. Functions that are wrapped must support the self._table_logger
attribute.

**Arguments**:

- `operation` _str_ - The name of the operation to be logged. This will be included in the log messages.
  

**Returns**:

- `inner_decorator` - A decorator that can be used to wrap a function that performs an operation on a table.
  

**Example**:

```python
@table_log_decorator(operation='delete_physical_data_for_table')
def _delete_physical_data(self, table: Table):
    self._dbutils.fs.rm(table.location, recurse=True)
```

