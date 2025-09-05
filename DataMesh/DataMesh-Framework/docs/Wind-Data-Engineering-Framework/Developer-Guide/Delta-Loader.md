# Delta Loader

The DeltaLoader allows to make incremental reads on a Delta table. There are
various possible strategies to use when reading increments of a table. One
possibility is to use the Change Data Feed feature to read the changes performed
on a table, e.g. to replay them on a target table. Another option is to read the
table and filter on a time column.

Independent of the strategy used, some metadata must be stored for the
DeltaLoader, so it can pick up on the last read version or timestamp. These
metadata are stored in a separate metadata table.

## Design

The DeltaLoader implementation follows a modular and extensible architecture,
designed to handle different strategies for loading data from Delta tables. It
makes use of the factory pattern to create the correct delta loader based on the
configured options.

This architecture can easily accommodate new loading strategies by adding new
classes that implement the DeltaLoader interface and updating the
DeltaLoaderFactory to recognize the new strategies.

:::mermaid
classDiagram
    class DeltaLoader {
        <<interface>>
        +str table_identifier
        +str delta_load_identifier
        +str metadata_table_identifier
        +get_data(dict<str,str> options)* DataFrame
    }

    class DeltaCDFLoader {
        +DeltaCDFConfig config
        +get_data(dict<str,str> options) DataFrame
    }

    class DeltaTimestampLoader {
        +DeltaTimestampConfig config
        +get_data(dict<str,str> options) DataFrame
    }

    class DeltaCDFConfig {
        +int from_version
        +int to_version
        +list<Column> deduplication_columns
    }

    class DeltaTimestampConfig {
        +Column timestamp_column
        +int from_timestamp
        +int to_timestamp
    }

    class DeltaLoadOption {
        +str strategy
        +str delta_load_identifier
        +dict<str, any> strategy_options
        +from_yaml_str(str)$ DeltaLoadOption
        +from_file(str)$ DeltaLoadOption
    }

    class DeltaLoaderFactory {
        +create_loader(DeltaLoadOption option) DeltaLoader
    }

    class DeltaLoaderMetadataTable {
        +str identifier
    }

    DeltaLoader <|-- DeltaCDFLoader
    DeltaLoader <|-- DeltaTimestampLoader
    DeltaCDFLoader o-- DeltaCDFConfig
    DeltaTimestampLoader o-- DeltaTimestampConfig
    DeltaLoaderFactory o-- DeltaLoadOption
    DeltaLoaderFactory --> DeltaLoader : creates
    DeltaLoader --> DeltaLoaderMetadataTable : writes into
:::
