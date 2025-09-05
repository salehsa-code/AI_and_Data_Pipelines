# Table of Contents

* [session\_manager](#session_manager)

<h1 id="session_manager">session_manager</h1>

This module defines a SessionManager class for managing Spark and DBUtils sessions.

<h2 id="session_manager.SessionManager">SessionManager</h2>

```python
class SessionManager()
```

A class used to manage Spark and DBUtils sessions.

**Attributes**:

- `_spark` - Stores the SparkSession instance.
- `_dbutils` - Stores the DBUtils instance.
  

**Methods**:

- `get_spark_session(config=None)` - Gets or creates a SparkSession instance.
- `get_dbutils()` - Gets or creates a DBUtils instance.

<h4 id="session_manager.SessionManager.get_spark_session">get_spark_session</h4>

```python
@classmethod
def get_spark_session(cls, config=None)
```

Get or create a SparkSession instance.

Requires a databricks sdk profile to be configured for local development.

**Arguments**:

- `config` _dict_ - A dictionary of Spark session configuration options.
  

**Returns**:

- `SparkSession` - The SparkSession instance.
  

**Raises**:

- `RuntimeError` - If the SparkSession instance cannot be created.

<h4 id="session_manager.SessionManager.get_dbutils">get_dbutils</h4>

```python
@classmethod
def get_dbutils(cls)
```

Get or create a DBUtils instance.

**Returns**:

- `DBUtils` - The DBUtils instance.
  

**Raises**:

- `RuntimeError` - If the DBUtils instance cannot be created.

