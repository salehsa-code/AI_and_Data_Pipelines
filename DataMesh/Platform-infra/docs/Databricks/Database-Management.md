# Database and Table Management

Database management (referred to as "schema" in Databricks) and table management
in the Wind Data and Analytics Platform (WDAP) were discussed at Center Court,
focusing on two main topics:

- How is the ownership of schemas organized in WDAP?
- How is the physical data underlying the tables in Databricks managed?

## Ownership of Schemas

Ownership of data is a crucial aspect of governing a data platform. In WDAP,
data is organized into layers:

- The first layer is for source data.
- The second layer contains primary & secondary data products.

The IAC framework supports the creation of new sources and new data products.
The owner of the schema is also the owner of the source/data product.

In some instances, primary data products may benefit from shared tables. These
should then be placed in a separate schema owned by the *Data Kong* Team.

## Management of Data Lake Objects

Databricks offers the use of "Managed Tables." Utilizing managed tables frees
the developer from worrying about the underlying files in the data lake. In some
cases, managed tables may also enhance performance because the Databricks
framework has complete control over data storage, whereas with "External
Tables," Databricks only manages the metadata.

The advantage of external tables is their ease of use outside Databricks. This
is why the current approach within WDAP is to exclusively use external tables.
The IAC and data engineering frameworks are designed to assist developers in
managing the objects in the data lake underlying the tables.

A potential drawback of this decision is that some features in Databricks are
currently only available for managed tables. It is also possible that Databricks
will introduce more features exclusive to "Managed Tables" in the future. But
Databricks ensured, that over the long period there will be feature parity
between external and managed tables.
