# Power BI Datasources

Datasources are derived from the [Power BI data gateways](./Data-Gateways.md).

## WDAP Datasources

| Datasource Name | Data Gateway | Owner |
| --- | --- | --- |
| --- | **DEV/TST** | --- |
| WDAP_ADEPT_DEV | WindPBIGatewayClusterDevTst | ADEPT Team |
| --- | **ACC/PRD** | --- |

## Provisioning of Datasources

The datasources are initially provisioned by the platform team and set up with
dummy credentials. Datasources will be created on demand for the value delivery
teams in the required environments. If not otherwise aligned, the
`vap2_<env>_pbi_serverless_warehouse` SQL endpoint should be used.

### Authentication

Authentication should be configured using OAuth 2.0 with a dedicated s7 user.
Ensure that the s7 user has the correct permissions on the WDAP workspaces and
catalogs by having it in a group that provides that access.
