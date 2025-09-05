# Metadata

WinDEF is a metadata-driven framework. Metadata is used to configure the data
schema as well as the pipelines. The metadata is stored in `YAML` files and is
loaded into the framework at runtime. Where the metadata is stored is
configurable. A best practice seems to be to define the metadata in the data
products repository and deploy it to an ADLS using the CI/CD pipeline. The
framework will then consume it using a Volume mounting the ADLS.

## Metadata References

Find references for the different metadata objects here:

- [Schemas](../../Data-Contract.md#data-contract-reference): Defines a schema in
  Unity Catalog and related resources.
- [Tables](../../Data-Contract.md#dataset-reference): Defines a table in Unity
  Catalog.
- [Pipelines](../../Developer-Guide/Pipelines.md): Defines an ETL with 0 to N
  sources and targets.
