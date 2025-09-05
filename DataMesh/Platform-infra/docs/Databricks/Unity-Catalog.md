# Unity Catalog

[[_TOC_]]

## Scope

This article is related to [PBI 276480](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_sprints/taskboard/Data%20Farmers/VAP2-WIND-DataAnalytics/Sprint%2024%20-%2021%20Sep%20-%204%20Oct?workitem=276480) and aims to answer these questions:

- What objects are introduced in Unity Catalog?
- How are objects in Unity Catalog structured?
- What changes do I need to be aware of when migrating notebooks/jobs?

## Unity Catalog Objects

![Unity Catalog Objects](../.img/unity-catalog/unity-catalog-objects.drawio.png)

The above image shows the most relevant objects within Unity Catalog. A full overview can be taken from the [Microsoft Documentation](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/privileges#--securable-objects-in-unity-catalog).

All Unity Catalog objects exist within the _Account_. **Account Admins** can manage all objects within the Account, i.e., User Management, Access Management and Metastore(s). In Vattenfall currently there is no ownership of the Account defined. For Account level tasks, such as assigning new AD groups or creating new catalogs, reach out to David Achilles (<bet60@eur.corp.vattenfall.com>) or Alexander Fröhlich (<bka27@eur.corp.vattenfall.com>).

### Metastore

The top-level container for metadata. Databricks restricts the deployment of Metastores to one per cloud region. This means for Vattenfall there is only a single Metastore. Data can be exchanged between Catalogs in the same Metastore. **Metastore Admins** can manage a Metastore.

Note: Currently, the roles of _Account Admin_ and _Metastore Admin_ overlap significantly, with no specific _Metastore Admins_ assigned in VF.

### Storage Credential & External Location

**Storage Credentials** are long-term cloud credentials that provide access to cloud storage, e.g., ADLS. Permissions on this object allow low-level interactions with the ADLS, like reading and writing files.​ Storage Credentials can be created either with the Access Connectors' Managed Identity or with a Service Principal Secret. We prefer the Managed Identity, because in general identity based authentication is more secure than key based authentication and it removes the need to rotate secrets.

**External Locations** contain a reference to a storage credential and a cloud storage path. Permissions on this object allow low-level interactions with the ADLS, like reading and writing files.

Note: No _External Locations_ for overlapping paths can be created. This implies that you can't create one External Location for a container and another one for a folder within the same container.

### Catalog, Schema & Tables/Views

**Catalogs** can be compared to the Hive Metastore, but they are independent from a Workspace. A Catalog exposes a 3-layer-hierarchy of [catalog].[schema].[table]. The overall number of Catalogs per Metastore is limited; therefore it is not possible to deploy a catalog for each and every usecase.

**Schemas** are sometimes referred to as "Database" in the Databricks documentation. They present the second layer of the object hierarchy.

**Tables/Views** represent the lowest level in the object hierarchy. There is a difference between External and Managed Tables that developers need to consider. See the section below to understand why we almost always prefer External Tables. Only create Managed Tables when there is a very good reason.

#### External Tables vs. Managed Tables

**External Tables**:

- are essentially pointers to ADLS storage locations.
- store only metadata in the Metastore/Storage Root.
- remove only the metadata when dropping the table.

Create a Table with a reference to the storage Location, as follows:

```SQL
CREATE TABLE <catalog>.<schema>.<table-name>
(
  <column-specification>
)
LOCATION 'abfss://<bucket-path>/<table-directory>';
```

**Managed Tables**:

- are managed by Databricks
- are stored in the root storage of the catalog or schema, but identified with a unique identifier
- support more features, sooner, when compared to External Tables

Create a Table directly in the Catalog, as follows:

```SQL
CREATE TABLE <catalog>.<schema>.<table-name>
(
  <column-specification>
)
```

**Why We Prefer External Tables**:

- They prevent **vendor lock-in**. Managed Tables, although stored in our ADLS,
  have complex structures that make integrations challenging.
- External tables **simplify integration** with other tools by granting direct
  access to ADLS for future use-cases.
- Managed tables risk **data duplication** if original data is also stored in
  ADLS.

## Metastore, Catalog and Workspace Relations

![Unity Catalog Objects](../.img/unity-catalog/unity-catalog-relations.drawio.png)

**Metastore** → **Catalog**: Catalogs exist inside the Metastore.

**Metastore** → **Workspace**: Workspaces must be assigned to a Metastore to
interact with UC objects.

**Catalog** → **Workspace**: A common misunderstanding is the idea that there is
a relationship between the Catalog and the Workspace, but there is **NONE**,
other than the relatively unimportant workspace binding! Catalogs might define
bindings; those would define which Workspaces can interact with the Catalog.

### Examples

Consider a setup where a User with `USE_CATALOG` permission on Catalog `A` wants
to query the catalog to get a schema metadata:

```sql
SELECT * from A.information_schema.schemata
```

This query would fail if the workspace from which the User is executing the
query is not onboarded to Unity Catalog (i.e., not assigned to a Metastore), or
if the Catalog defines a workspace binding that excludes this Workspace.

## Clusters

Cluster requirements for interacting with the Catalog:

- Access Mode: Shared or Single User (USER_ISOLATION in API)
- Credential passthrough is not supported
- Must run on Databricks Runtime 11.3 LTS or higher

Access Modes:

- Single User: Assigned for the exclusive use of one user
- Shared: Available for multiple users with guaranteed data isolation. _Requires
  a premium Workspace.

> *Note*: All SQL Warehouses can interact with Unity Catalog by default.

Refer to [Databricks
docs](https://docs.databricks.com/en/data-governance/unity-catalog/compute.html)
for the full list of limitations.

## Unity Catalog @ Vattenfall & WDAP

![Unity Catalog implementation at Vattenfall](../.img/unity-catalog/unity-catalog-at-vattenfall.drawio.png)

The central implementation of Unity Catalog (UC) consists of:

1. SCIM Integration with AAD
1. A single Metastore for each tenant, which is shared across all of VF
1. Catalog Deployments

None of the resources in the Unity Catalog are directly used by the projects,
but they are crucial for the system to work. Each project will have its own Root
Storage and Access Connector.

Difference to non-UC integrated workspaces: SCIM is managed centrally.
Therefore, to add a new AD group to a Workspace or Catalog Object, one must
request this from a Account Admin.

## Physical Data Structure in WDAP

![Unity Catalog physical data structure in WDAP](../.img/unity-catalog/unity-catalog-physical-data-structure.drawio.png)

The displayed visualization represents the physical data structure. While the
logical data structure might vary in detail, it should largely mirror this to
ensure maintainability and avoid confusion.

Important Considerations:

- Avoid sourcing tables in one schema from multiple external locations unless
  there's a very good reason (I can’t imagine any reason to do so).
- External Locations typically have 0-1 schema mapped. For instance, the landing
  zone has an external location but not a schema.
