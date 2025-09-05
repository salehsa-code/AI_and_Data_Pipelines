# Delta Loader

The `DeltaLoader` is a tool designed to perform incremental reads on a Delta
table. It supports various strategies for reading increments, such as using the
Change Data Feed (CDF) feature to capture changes or filtering based on a time
column. The `DeltaLoader` ensures that metadata is stored to keep track of the
last read version or timestamp, allowing for seamless continuation of data
loading.

## Usage

- **Configuration**: Define the loading strategy and options using
  `DeltaLoadOption`.
- **Loader Creation**: Use `DeltaLoaderFactory` to create the appropriate loader
  from your `DeltaLoadOption`.
- **Data Retrieval**: Call `get_data` on the loader to retrieve the data.
- **Metadata Management**: The loader updates the metadata table to track the
  last read version or timestamp.

### Strategies

Currently, two strategies for `DeltaLoader` are implemented, `DeltaCDFLoader`
and `DeltaTimestampLodaer`.

- [Scenarios](./Delta-Loader/Scenarios.md): Scenarios, the delta loader feature might be used in

#### DeltaCDFLoader

The `DeltaCDFLoader` reads changes on the source table from the Change Data
Feed. This feature needs to be enabled on the table for the `DeltaCDFLoader` to
work. To enable it, set the table property `delta.enableChangeDataFeed = true`.
Only changes applied to the table after the Change Data Feed is enabled can be
used. There is however an option for the `DeltaCDFLoader` to do an initial full
load of the table, `enable_full_load`. Read more
[here](./Delta-Loader/DeltaCDFLoader.md).

The `DeltaCDFLoader`is represented by the `DeltaCDFConfig`, see the
[reference](../../Reference/data_handling.md) for more details.

#### DeltaTimestampLoader

The `DeltaTimestampLoader` reads data from a table and filters on a timestamp
column. This allows to incrementally read new data by picking up from the last
read timestamp. This strategy is most useful for reading timeseries data that
does not require updates on previous records. However, workflows based on the
`_metadata.file_modification_time` can also be possible. Read more
[here](./Delta-Loader/DeltaTimestampLoader.md).

The `DeltaTimestampLoader` is represented by the `DeltaTimestampConfig`, see the
[reference](../../Reference/data_handling.md) for more details.

### Which Strategy to Use?

The following flowchart should help you decide which delta load strategy to use
for your delta load opeartion.

:::mermaid
flowchart TD
    A[Start] --> B{"Is the data timeseries?"}
    B -->|Yes| C{"Do you need to update old records?"}
    B -->|No| D["Use Change Data Feed (CDF) Strategy"]
    C -->|Yes| D
    C -->|No| E["Use Timestamp-Based Strategy"]
:::
