# DeltaTimestampLoader

The `DeltaTimestampLoader` class allows to perform delta loads using one or more
timestamp columns.

## Delta Loader metadata

The transaction history is kept in a Delta Loader metadata table. Delta
loads from a source table are registered in this metadata table, tracking the
last read timestamp. A `delta_load_identifier` is used to distinguish
different loads from the same source table, e.g. if data from the same source
table is used in different pipelines. If a delta load was successful, the entry
for this load is updated and the `is_processed` column is set to true, so that
following delta loads know where to continue.

## How To: Incrementally append to a target table

The following example reads from a source table using the Timnestamp strategy
and appends to a target table.

```python
from windef.data_handling import DeltaLoadOption, DeltaLoaderFactory, DeltaManager

# Create Delta Loader
delta_manager = DeltaManager()
timestamp_delta_load_options = DeltaLoadOptions(
    strategy="Timestamp",
    delta_load_identifier="example_delta_load_identifier",
    strategy_options={
        "timestamp_filter_cols": ["timestamp_col"],
    },
)
loader = DeltaLoaderFactory.create_loader(
    table_identifier=source_table.identifier,
    options=timestamp_delta_load_options,
)

# Read Data Using Delta Load Strategy
df = loader.get_data()

# Write Data to Target Table
delta_manager.append_dataframe(
    table=target_table,
    data_frame=df,
)

# Mark Delta Load as Processed
loader.consume_data()
```

## Technical Description

This section covers the technical implementation of the `DeltaTimestampLoader` in
detail.

The general workflow of the `DeltaTimestampLoader` is following these steps:

1. Get `timestamp` to start reading from.
    - *Metadata table has entries for `source_table` and
      `delta_load_identifier`?
        - *Yes*:
            - Get latest `last_read_timestamp` that is processed and not stale
        - *No*:
            - Don't use a lower bound.
    - (*Optional*): If custom bounds (`from_timestamp`, `to_timestamp`) are set,
      the lower bound is adjusted accordingly.
1. Read data from source table filtering on the `start_timestamp`
    - (*Optional*) If custom upper bound (`to_timestamp`) is set, filter also on
      that.
1. Register read operation in `DeltaTimestampLoader` metadata table.
    - Create new entry with `last_read_timestamp` current timestamp (or
      `to_timestamp` if set) and set `is_processed` to false.
1. (*Optional*) Apply Transformations to data frame
1. Write data to target table(s)
    - Perform all write operations
    - If writes were successful, the delta load entry in the DeltaLoaderCDF
      metadata table is marked as `is_processed`.
    - If any of the writes were not successful, changes to tables that were
      already applied have to be reverted to the previous table version.

The write operations are very individual to the specific usecase and cannot
easily be mapped to a wrapper function. In case the write is more complex than
writing to a single target table, the writing and consumption of data should be
handled manually instead of using the `write_data` wrapper on the delta loader.
