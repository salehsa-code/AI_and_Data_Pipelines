# Logging

## Overview

The logging module provides a simple interface to log messages
to the Log Analytics Workspace or the console. All components
of the Framework use this module to log messages. It could also be
used by application or notebook code to log messages.

## How To: Log a Message

The following example shows how to log a message:

```python
from windef.logging import LoggingService
import os

# These variables are preconfigured on clusters in the WDAP Workspaces
# and typically don't need to be changed
# os.environ['LOG_ANALYTICS_WORKSPACE_ID'] = 'your_workspace_id'
# os.environ['LOG_ANALYTICS_WORKSPACE_SHARED_KEY'] = 'your_shared_key'

# This is the name of the table of the LAW where the logs will be stored
os.environ['LOG_TYPE'] = 'example_log'

logger = LoggingService(log_to_azure=True).get_logger()

# values and columns are seperated by a colon respectively a pipe
# these seperators are configurable in the LoggingService
message = "first_column:first_value | second_column:second_value"
logger.info(message)
```

The above example would result in this log entry in the `EXAMPLE_LOG_CL`
table of the preconfigured Log Analytics Workspace:

| timestamp_s         | level | first_column_s | second_column_s |
| ------------------- | ----- | -------------- | --------------- |
| 2022-01-17 00:00:00 | INFO  | first_value    | second_value    |

Notice, that the log entry contains the timestamp and the level of the
log entry. These columns are added automatically by the Log Analytics
Handler, that is added to the logger when `log_to_azure` is set to True.

> Besides these columns, the log entry would of course contain additional
> columns, that are automatically added by the Log Analytics Workspace.

## How To: Customize the Logger

The `LoggingService` provides a few options to customize the logger.

These attributes can be set in the constructor of the `LoggingService`:

| Parameter | Description |
| ---- | ---- |
| `logger_name` | The name of the logger to be created. Defaults to the name of the calling module. |
| `log_level` | The log level of the logger. Defaults to `INFO`. I.e. messages with a log level of `INFO` or higher will be logged. |
| `workspace_id` | ID of the Log Analytics Workspace. Defaults to the value of the environment variable `LOG_ANALYTICS_WORKSPACE_ID`. |
| `shared_key` | Shared key of the Log Analytics Workspace. Defaults to the value of the environment variable `LOG_ANALYTICS_WORKSPACE_SHARED_KEY`. |
| `log_type` | Name of the table in the Log Analytics Workspace where the logs will be stored. Defaults to the value of the environment variable `LOG_TYPE`. |
| `column_split_char` | Character that is used to split the columns of the log message. Defaults to ` |
| `key_value_split_char` | Character that is used to split the key and value of a column. Defaults to `:`. |
| `test_connectivity` | If set to `True`, the logger will try to connect to the Log Analytics Workspace. If the connection fails, an exception will be raised. Defaults to `True`. |
| `log_to_azure` | If set to `True`, the logger will log messages to the Log Analytics Workspace. Defaults to `True`. |
| `log_to_console` | If set to `True`, the logger will log messages to the console. Defaults to `True`. |
