# Scenarios

The following scenarios are examples to help understanding how the Delta Loader
operates.

We assume the following table as our source table:

Source Table

| Source Table  |
| :------------ |
| id_col        |
| partition_col |
| value_col     |

The `id_col` column is the key of the table, it cannot be null and must be
unique. The `partition_col` column is used for partitioning, it cannot be null.
The `value_col` column holds values, there are no constraints on this column.

For simplicity, we assume that we always write to a target table with the same
schema.

## CDF Scenarios

### Case 1 - Create Fresh Delta Transaction

The source table is created and some initial data is inserted into the table.
The table history contains the following entries

Table History:

| version | action       |
| ------- | ------------ |
| 0       | CREATE TABLE |
| 1       | INSERT INTO  |

We want to load the data into our target table, using the delta loader identity
"target_table_identifier".

The Delta CDF Loader metadata table contains no entries for this delta loader
identity.

Delta Loader Metadata:

| start_commit_ver | end_commit_ver | is_processed | is_stale |
| ---------------: | -------------: | ------------ | -------- |
|         // empty |                |              |          |

**Expected behavior:**

We read data from the source table starting from version 0 and ending with
version 1. After the transaction is completed we expect the following entry in
the Delta Loader metadata table.

Delta Loader Metadata:

| start_commit_ver | end_commit_ver | is_processed | is_stale |
| ---------------: | -------------: | ------------ | -------- |
|                0 |              1 | true         | false    |

### Case 2 - Delta Load without changes

The source table is created and some initial data is inserted into the table.
The target table was loaded as shown in [Case
1](#case-1---create-fresh-delta-transaction). The table history contains the
following entries

Table History:

| version | action       |
| ------- | ------------ |
| 0       | CREATE TABLE |
| 1       | INSERT INTO  |

The target table was loaded using the Delta CDF Loader and the delta load was
recorded in the Delta Loader metadata table.

Delta Loader Metadata:

| start_commit_ver | end_commit_ver | is_processed | is_stale |
| ---------------: | -------------: | ------------ | -------- |
|                0 |              1 | true         | false    |

**Expected behavior:**

No new data is read from the source table and the target table remains
unchanged. After the transaction is completed, we expect the following entries
in the Delta Loader metadata table.

Delta Loader Metadata:

| start_commit_ver | end_commit_ver | is_processed | is_stale |
| ---------------: | -------------: | ------------ | -------- |
|                0 |              1 | true         | false    |
|                1 |              1 | true         | false    |

### Case 3 - Merge with Deduplication

The source table is created and some initial data is inserted into the table,
then a few rows are updated. We want to start a delta load to the target table
using "MERGE". The table history contains the following entries

Table History:

| version | action       |
| ------- | ------------ |
| 0       | CREATE TABLE |
| 1       | INSERT INTO  |
| 2       | MERGE INTO   |

No previous delta loads were applied to the target table, so the version history
is empty.

Delta Loader Metadata:

| start_commit_ver | end_commit_ver | is_processed | is_stale |
| ---------------: | -------------: | ------------ | -------- |
|         // empty |                |              |          |

**Expected behavior:**

The inserted and updated rows are read from the source table. Then, the read
data is deduplicated, returning only the newest version for each unique value in
`id_col`. This data is merged into the target table. The Delta Load metadata
table contains the following entry.

Delta Loader Metadata:

| start_commit_ver | end_commit_ver | is_processed | is_stale |
| ---------------: | -------------: | ------------ | -------- |
|                0 |              2 | true         | false    |

> :warning: The Delta CDF Loader currently does not support deletes on the
> target table. Any rows deleted in the source table will still be written to
> the target table or remain there. To enable this feature, the CDF metadata
> columns must not be stripped and the entries with `update_preimage` change
> type must be kept in the read method and a dedicated merge method must be
> implemented that extracts the data to be deleted using the CDF metadata.

## Timestamp Scenarios

### Case 1 - Create Fresh Timestamp Transaction

The source table is created and some initial data is inserted into the table.
The table history contains the following entries.

Table History:

| version | action       |
| ------- | ------------ |
| 0       | CREATE TABLE |
| 1       | INSERT INTO  |

We want to load the data into our target table, using the delta loader identity
"target_table_identifier".

The Delta Loader metadata table contains no entries for this delta loader
identity.

Delta Loader Metadata:

| last_read_timestamp | is_processed | is_stale |
| ---------------: | -------------: | ------------ |
|         // empty |                |              |

**Expected behavior:**

We read data from the source table starting from 2025-01-01 to 2025-01-02.
After the transaction is completed we expect the following entry the
Delta Loader metadata table.

Delta Loader Metadata:

| last_read_timestamp | is_processed | is_stale |
| ---------------: | -------------: | ------------ |
|     2025-01-02   | true         | false    |

### Case 2 - Timestamp Load without changes

The source table is created and some initial data is inserted into the table.
The target table was loaded as shown in [Case
1](#case-1---create-fresh-timestamp-transaction) The table history contains the
following entries

Table History:

| version | action       |
| ------- | ------------ |
| 0       | CREATE TABLE |
| 1       | INSERT INTO  |

The target table was loaded using the Delta Timestamp Loader and the delta load was
recorded in the Delta Loader metadata table.

Delta Loader Metadata:

| last_read_timestamp | is_processed | is_stale |
| ---------------: | -------------: | ------------ |
|     2025-01-02   | true         | false    |

**Expected behavior:**

No new data is read from the source table and the target table remains
unchanged. After the transaction is completed, we expect the following entries
in the Delta Loader metadata table.

Delta Loader Metadata:

| last_read_timestamp | is_processed | is_stale |
| ---------------: | -------------: | ------------ |
|     2025-01-02   | true         | false    |
|     2025-01-02   | true         | false    |
