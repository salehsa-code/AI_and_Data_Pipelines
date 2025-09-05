# DeltaCDFLoader

The `DeltaCDFLoader` class allows to perform delta loads using the delta change
data feed metadata.

## Requirements

The `DeltaCDFLoader` requires that the `delta.enableChangeDataFeed` option is set
to `true` for the source table.

## Delta Loader metadata

The transaction history is kept in a Delta Loader metadata table. Delta loads
from a source table are registered in this metadata table, tracking the start
and end commit versions. A `delta_load_identifier` is used to distinguish
different loads from the same source table, e.g. if data from the same source
table is used in different pipelines. If a delta load was successful, the entry
for this load is updated and the `is_processed` column is set to true, so that
following delta loads know where to continue.

## How To: Incrementally update a target table

> :warning: The `DeltaCDFLoader` currently does **not** support deletes on the
> target table. Any rows deleted in the source table will still be written to
> the target table or remain there.

The following example reads from a source table using the CDF strategy and
updates a target table.

```python
from windef.data_handling import DeltaLoadOption, DeltaLoaderFactory, DeltaManager

# Create Delta Loader
delta_manager = DeltaManager()
cdf_delta_load_options = DeltaLoadOptions(
    strategy="CDF",
    delta_load_identifier="example_delta_load_identifier",
    strategy_options={
        "deduplication_columns": ["id_col"],
    },
)
loader = DeltaLoaderFactory.create_loader(
    table_identifier=source_table.identifier,
    options=cdf_delta_load_options,
)

# Read Data Using Delta Load Strategy
df = loader.get_data()

# Write Data to Target Table
delta_manager.merge_dataframe(
    table=target_table,
    data_frame=df,
    key_columns=["id_col"],
)

# Mark Delta Load as Processed
loader.consume_data()
```

## Technical Description

This section covers the technical implementation of the `DeltaCDFLoader` in
detail.

The general workflow of the `DeltaCDFLoader` is following these steps:

1. Get start and end commit versions for the read action.
    - Determine minimum and maximum commit version from source table history
        - `min_commit_version`: Latest version where `CREATE`, `TRUNCATE`
          operation was performed or `delta.enableChangeDataFeed` was enabled.
        - `max_commit_version`: Latest version in table history.
    - *Metadata table has entries for `source_table` and
      `delta_load_identifier`?
        - *Yes*:
            - Get latest `end_commit_version` that is processed and not stale
            - Use greater of `end_commit_version` or `min_commit_version` as new
              `start_commit_version`
        - *No*:
            - Use `min_commit_version` and `max_commit_version` for new
              `start_commit_version` and `end_commit_version`
1. Read data from source table using `start_commit_version` and
   `end_commit_version` and including delta CDF metadata.
    - Is `start_commit_version == end_commit_version`?
        - *Yes*: return empty data frame
        - *No*: read data from source table starting from
        `start_commit_version+1`, ending at `end_commit_version`. We increment
        `start_commit_version` by 1 to avoid reading this version twice.
    - (*Optional*) deduplicate dataframe. This is only necessary if there is a
      unique key column and if the source table can contain updates.
    - Strip delta CDF metadata columns.
1. Register read operation in `DeltaCDFLoader` metadata table.
    - Create new entry with `start_commit_version` and `end_commit_version` and
      set `is_processed` to false.
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
