# WinDEFDataFrameWriter Class User Guide

The `WinDEFDataFrameWriter` class provides functionalities for writing Spark
DataFrames in a specified format to a certain location. This guide will help you
understand how to use the class to perform different operations on data frames.

> :warning: The `WinDEFDataFrameWriter` itself is only a base class without
> actual implementation. There currently is one implementation, that implements

Find a reference of all methods used in this guide
[here](../../../Reference/data_handling.md).

## Available writer

There are currently three implementation of the `WinDEFDataFrameWriter`.

- `FileDataFrameWriter`: used to write files from a data frame to a location on
  a data lake.

## How To: Write a DataFrame as a Stream

To write a DataFrame to a specified location in a specified format as a stream,
you can use the `write_stream()` method. This method takes several parameters
including the DataFrame to write, the location to write to, the format of the
file, the location of the checkpoint, the columns to partition on, whether to
merge schema, the mode, the trigger, the trigger specification, and additional
DataFrame writer options.

```python
writer.write_stream(data_frame, location="path/to/location", format="delta")
```

## How To: Write a DataFrame

To write a DataFrame to a specified location in a specified format, you can use
the `write()` method. This method takes several parameters including the
DataFrame to write, the location to write to, the format of the file, the
columns to partition on, the mode, and additional DataFrame writer options.

```python
writer.write(data_frame, location="path/to/location", format="delta")
```
