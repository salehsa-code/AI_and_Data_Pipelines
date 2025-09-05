# Add Value Delivery Team Customer Permissions

Value Delivery Teams (VDT) can grant access to their schemas by modifying the
`grants.yml` file as described
[here](../IaC-Framework/Solutions/21-Data-Product.md).

## Catalog Access

Customers will at least also require the `USE_CATALOG` privilege. This can be
configured in the `catalogs.yml`, which is part of the `12` solution. Add a new
line under the `user_groups` key of the relevant catalog(s). The key must be the
group name or service principal Application Id, the value can be an empty list.

## SQL Warehouse Access

Additionally customers might need access to Compute in the form of a SQL
Warehouse. This can be configured in the `sql_warehouses.yml`, as described
[here](../IaC-Framework/Solutions/12-Databricks-Config.md). The key must be
the group name or service principal Application Id, the value should be the
required permission, e.g. `CAN_USE`.
