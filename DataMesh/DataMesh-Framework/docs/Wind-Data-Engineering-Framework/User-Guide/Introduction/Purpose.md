# Purpose

## Motivation

There is a lot of talent and a lot knowledge when it comes to data engineering
within BA Wind and Asset IT. However, there is not yet an easy way of sharing
solutions to common data engineering problems. Also, there is no single aligned
way of dealing with topics that need to be addressed by any project that
includes data processing like monitoring and maintenance.

The idea of the Wind Data Engineering Framework (*WinDEF*) is to fill this gap
with a collection of artefacts and processes that implement best practices. It
is meant to be an evolutionary developing framework which means that it should
integrate learnings from different data engineering teams such that every team
can benefit from it.

Some data engineering tasks are repetitive. They require the same steps to be
executed but with different metadata information like the name of a table or
columns to select from. For such cases, the framework offers high-level building
blocks that can be configured to the specific needs of a data engineer simply by
configuring different values of metadata as parameters.

But even more complex tasks like data validation, data transformation, or SCD2
merges can be implemented with the framework.

Some WinDEF benefits over using custom code are:

- **Swarm Intelligence**: One smart person has to solve a problem once, and
  everyone benefits from it.
- **Efficiency and Time-Saving**: Utilizing a framework eliminates the need to
  repetitively code common tasks.
- **Standardization and Consistency**: The use of a framework ensures
  standardization across teams, which leads to more consistent code and easier
  maintenance.
- **Enhanced Collaboration**: Sharing the same framework across different teams
  promotes collaboration and knowledge sharing, which leads to a more effective
  and efficient work environment.
- **Improved Quality**: By having multiple people or teams test and maintain the
  code, bugs are more likely to be detected and fixed, enhancing the overall
  quality of the code.

## Concepts

### Using parts of WinDEF in Custom Code

When using WinDEF you can use the high-level building blocks to support your
custom code. If you just can't remember how the Power BI REST API works you can
e.g. use the `Power BI Client` to refresh a dataset once the data has landed. Or
you wan't to send logs to a Log Analytics Workspace but don't want to write a
lot of boilerplate code, you can use the `LogAnalyticsHandler` to do that.

Not all parts of the framework are available to use in custom code, because they
might have dependencies on other parts of the framework. Most parts of the
`data_handling` package for example require WinDEF specific `Table` objects that
can either be configured via Metadata or derived from the Unity Catalog
instance.

:::mermaid
graph LR
    A[Install WinDEF]
    B[Import Building Blocks]
    C[Use Building \nBlocks in Custom Code]
    D[...]

    A --> B --> C --> D
:::

### Using WinDEF as a Framework

When using WinDEF as a framework you configure the Metadata for your data and
pipelines and let the framework do the rest.

:::mermaid
graph LR
    A[Install WinDEF]
    D[Import PipelineService]
    B[Configure Metadata]
    C[Run Pipeline]

    A --> D
    D --> C
    B --> C
:::

## Assumptions

WinDEF is designed with the Wnd Data & Analytics Platform in mind. As such it is
making some assumptions on the surrounding technical setup:

1. *Spark* is the main data engineering tool.
2. *PySpark* is the main way if interacting with the *Spark* engine.
3. *Azure Databricks* is the *Spark* implementation we are using. The Workspace
   is onboarded to a Metastore.
4. *Azure Data Lake Storage* is the main data storage.
5. *Environment Variables* are used to configure the framework, e.g. the
   connectivity to the Log Analytics Workspace.
