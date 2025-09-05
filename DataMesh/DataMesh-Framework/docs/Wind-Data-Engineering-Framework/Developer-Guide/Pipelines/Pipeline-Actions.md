# Pipeline Actions

This guide provides a step-by-step process for developers to implement new
`PipelineAction` subclasses in the ETL pipeline Python package.

## Concept

A `PipelineAction` is the base class for all actions in the ETL pipeline. Each
action performed in the pipeline is a subclass of `PipelineAction`.

Each `PipelineAction` subclass must implement a `run` method which defines how
the action is executed. The `run` method takes a `PipelineContext` object as an
argument, which encapsulates the state of the pipeline, including data and
metadata.

## Steps to Implement a New `PipelineAction` Subclass

1. **Define the subclass**: Start by defining a new subclass of
   `PipelineAction`. The name of the subclass should represent the action it
   performs.

```python
from ..pipeline import PipelineAction, PipelineContext

class NewAction(PipelineAction):
    pass
```

2. **Set the `name` attribute**: Each subclass must have a `name` attribute.
   This attribute is used to identify the action.

```python
class NewAction(PipelineAction):
    name: str = "NEW_ACTION"
```

3. **Implement the `run` method**: The `run` method is where the action is
   defined. It should take a `PipelineContext` object as its first argument,
   followed by any other arguments required for the action.

   > To enforce keyword arguments, please define the arguments accoringly and
   > mind the `*`.

```python
class NewAction(PipelineAction):
    name: str = "NEW_ACTION"

    @staticmethod
    def run(context: PipelineContext, *, arg1, arg2, ...):
        pass
```

4. **Define the action**: The action is defined within the `run` method. It must
   return `PipelineContext`. If the `PipelineContext` was changed as part of the
   Action, make sure to return the updated Context.

```python
class NewAction(PipelineAction):
    name: str = "NEW_ACTION"

    @staticmethod
    def run(context: PipelineContext, arg1, arg2, ...):
        # perform some action, e.g. on context.data or context.metadata
        # ...
        # return the PipelineContext
        return PipelineContext(metadata=new_metadata, data=new_data)
```

## Best Practices

- **Encapsulation**: Each `PipelineAction` subclass should encapsulate a single,
  specific action. This follows the Single Responsibility Principle and makes
  each action easy to understand and test.
- **Error Handling**: The `run` method should handle any errors that might occur
  during its execution. This might involve catching exceptions, validating
  input, or handling edge cases.
- **Tests**: Each action should be tested. Tests should run locally. Therefore,
  the test usually only checks, whether the action is calling the correct
  functions.
  > important actions can be tested in the Integration tests, this will allow
  > more meaningful Tests.

## Example

Here is an example of a `PipelineAction` subclass that filters a DataFrame based
on a condition:

```python
from ..pipeline import PipelineAction, PipelineContext

class FilterDataAction(PipelineAction):
    name: str = "FILTER_DATA"

    @staticmethod
    def run(context: PipelineContext, *, condition: str):
        # filter the data based on the condition
        new_data = context.data.filter(condition)

        # return a new PipelineContext with the filtered data
        return PipelineContext(metadata=context.metadata, data=new_data)
```

This action can now be used in a pipeline like so:

```yaml
id: New Action Pipeline
steps:
  # ... previous steps
  Filter Data:
    action: FILTER_DATA
      options:
        condition: "age > 15"
```
