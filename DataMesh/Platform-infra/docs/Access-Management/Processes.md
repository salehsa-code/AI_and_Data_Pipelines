# Processes

[[_TOC_]]

## Request Access to Azure Data Lake Storage (ADLS)

:::mermaid
graph LR
    A[Requester]
    B[Data Kongs]
    C[Platform Owner]
    D[Decision Point: Volume, ACL or RBAC]

    A -->  |Request Permission|C
    B -->  |Evaluate Request|D
    D --> |Grant Access| A
    C -->  |Inform about approval/denial|A
    C --> |Inform about requirement|B
:::

## Create an Omada Resource

![Process to create an Omada Resource](../.img/access-management/processes_create_omada_resource.drawio.png =900x)

## Request Business Application Access

![Process to create an Omada Resource](../.img/access-management/processes_business_application_request.drawio.png =900x)

## Request Data Product Access in Unity Catalog

![Process to create an Omada Resource](../.img\access-management\processes_unity_catalog_request.drawio.png =900x)
