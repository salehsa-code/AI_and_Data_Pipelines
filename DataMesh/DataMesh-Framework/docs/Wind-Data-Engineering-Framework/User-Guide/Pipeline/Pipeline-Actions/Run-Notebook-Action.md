# Run Notebook Action

This special pipeline action allows to run another notebook as a pipeline step.

> :information: This action should only be used to cover actions that cannot
> (yet) be performed using other pipeline actions. Due to the way DataFrames are
> passed between notebooks and the extra startup time to run the external
> notebook, this action is less efficient, than using a normal pipeline action.
>
> Also keep in mind, that any additional logging and creation of metrics cannot
> be guaranteed and have to be taken care by the external notebook.

## Concept

The way this action works is to create a temporary view from the current
DataFrame in context and pass the view name to the external notebook as a
parameter.

In the external notebook, the DataFrame can then be obtained from the temporary
view and transformed. Finally, the external notebook should create a new
temporary view from the transformed DataFrame and return the name of the
temporary view as an exit parameter, so that the DataFrame can be obtained in
the pipeline step and stored as a result.

## Prerequisites

In order for this pipeline action to function, the external notebook must
fulfill the following criteria:

- It must expect a parameter called `view_name`, which is the name of the
  temporary view that holds the current DataFrame.
- It must return the name of a temporary view as an exit string, so that the
  transformed DataFrame can be obtained.

## Example

This is an example how the code in your external notebook could look like:

```python
# Get the DataFrame
view_name = dbutils.widgets.get("view_name")
global_temp_db = spark.conf.get("spark.sql.globalTempDatabase")
df = spark.sql(f"SELECT * FROM {global_temp_db}.{view_name}")

# Transform the DataFrame
df_transformed = df.withColumn("value_squared", df.value * df.value)

# Return new TempView
df_transformed.createOrReplaceGlobalTempView("output_view")
dbutils.notebook.exit("output_view")
```
