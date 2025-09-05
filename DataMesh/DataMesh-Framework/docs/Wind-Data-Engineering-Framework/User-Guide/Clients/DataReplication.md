# Data Replication

The `DataReplicationService` is used to replicate data from one table to
another. It supports different modes of replication, such as append and merge,
and allows for different replication strategies. If the target table is already
managed by the data replication service, the service updates it with the latest
data from the source table. Otherwise, the service (re-)creates the target table
and loads the data from the source table using the desired mode and strategy.

A job is set up that runs the `DeltaReplicationService` based on the configured
job parameters. This job can be used as a self-service to replicate tables from
the production environment to the dev or acc environments.

## Configuration

The `DataReplicationConfig` class is used to configure the data replication
process. This guide will help you set up and use DataReplicationConfig with the
DataReplicationService.

### Parameters

The `DataReplicationConfig` uses the following paramters

| Parameter | Description|
| --- | --- |
| source_table_identifier | The identifier of the source table. |
| target_table_identifier | The identifier of the target table. |
| target_environment | The target environment (e.g., dev, tst, acc). |
| replication_strategy | The mode of replication (currently only supporting delta replication). |
| mode | The mode of replication (e.g., append, merge, overwrite). |
| delta_load_options | Options for the delta loader strategy. |
| filter_str | A filter string to apply to the source table. |
| merge_key_columns | The columns to merge on. |
| merge_cols_to_update | The columns to update. |
| merge_cols_to_insert | The columns to insert. |
| merge_cols_to_exclude | The columns to exclude. |
| merge_when_matched_update | Whether to update when matched. |
| merge_when_matched_delete | Whether to delete when matched. |
| merge_when_not_matched_insert | Whether to insert when not matched. |

### Creating Configuration from Widgets

You can create a `DataReplicationConfig` instance from Databricks widgets using
the from_widgets method. This option is used to load the `DataReplicationConfig`
in the data replication job mentioned above.
