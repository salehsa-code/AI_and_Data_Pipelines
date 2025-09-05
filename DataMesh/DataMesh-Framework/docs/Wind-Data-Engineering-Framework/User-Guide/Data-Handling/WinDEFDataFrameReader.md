# WinDEFDataFrameReader Module User Guide

The `WinDEFDataFrameReader` module provides a set of functionalities for reading
Spark DataFrames using PySpark. This guide will walk you through the process of
using the module to read various types of data.

> :warning: The `WinDEFDataFrameReader` itself is only a base class without
> actual implementation. There are multiple derived classes that implement
> capabilities to read files, Kafka or API endpoints.

Find a reference of all methods used in this guide
[here](../../../Reference/data_handling.md).

## Available reader

There are currently three implementation of the `WinDEFDataFrameReader`.

- `FileDataFrameReader`: used to read files from a datalake storage into a data
  frame.
- `KafkaDataFrameReader`: used to read data from a Kafka endpoint.
- `ApiDataFrameReader`: used to read data from an API endpoint. *This reader currently only supports normal reading, not streaming.*

## How To: Reading a Streaming DataFrame

To read a specified location as a stream and return a streaming DataFrame, you
can use the `read_stream()` method.

```python
df = reader.read_stream(location='path/to/location', format='delta', schema=schema_dict, options=options_dict)
```

## How To: Reading a DataFrame

To read a specified location and return a DataFrame, you can use the `read()`
method.

```python
df = reader.read(location='path/to/location', format='delta', schema=schema_dict, options=options_dict)
```

## How To: Reading a DataFrame based on Extension

To read a specified location and return a DataFrame based on the extension
provided, you can use the `read_by_extension()` method. This method parses top
level and sub level directories by default.

```python
df = reader.read_by_extension(location='path/to/location', schema=schema_dict, extension='csv', search_subdirs=True, options=options_dict)
```
