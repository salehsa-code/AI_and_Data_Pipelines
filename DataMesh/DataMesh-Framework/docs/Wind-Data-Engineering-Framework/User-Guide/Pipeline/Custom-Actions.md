# Defining Custom Actions

Usually (especially in the mid to long run), nessy should provide most necessary
actions to run your ELT workloads. BUT it is impossible to know all required
Reads, Transformations etc. upfront. Therefore, WinDEF provides the option to
define custom Actions and integrate them with the `PipelineParsingService`.
Create your own Action:

```python
from windef.pipeline import PipelineAction

class MyCustomAction(PipelineAction):
    name: str = "MY_CUSTOM_ACTION"
    def run(self, context):
        print("Running custom action")
        return context
```

These are the requirements towards your implementation:

1. The class must inherit from `PipelineAction`
2. The class must define the `name` attribute
3. The class must implement a `run` method that accepts a context argument and
   returns a context object

You can then use your action in the Pipeline Definition:

```yaml
    id: test
    steps:
      step_1:
        action: MY_CUSTOM_ACTION
```

When instantiating the `PipelineParsingService` you must register the action by
passing it into the constructor:

```python
# ... your action & pipeline definition as described above
p = PipelineParsingService([MyCustomAction]).parse_yaml(yaml_str=yaml_str)
p.run() # run the pipeline with your custom action
```

!!! note "Instantiating the PipelineParsingService"
    Notice, how `MyCustomAction` is passed as a list to the
    PipelineParsingService during instantiation
