# S7 Users on WDAP

On WDAP, s7 users should only be used in exceptional cases. One of these cases,
where it is not possible to use another way of authentication is for the Power
BI Gateways.

The s7 users are onboarded and synched to the platform using the
`z_azu_wdap_<envgrp>_<env>_s7users__a` Entra Id Groups. These groups are managed
through the IaC Framework (`10-platfrom_automation_core` solution). s7 users in
this group are automatically synched to the corresponding SRV workspace and
granted `USE CATALOG` access on the dataproducts and DLH catalogs. Additionally
they get permission to use the Power BI SQL Warehouse.
