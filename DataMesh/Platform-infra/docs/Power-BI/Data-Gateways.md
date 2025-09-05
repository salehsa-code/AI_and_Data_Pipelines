# Power BI Data Gateways

The Power BI data gateways are used to provide access to the SQL endpoints on
the WDAP Databricks workspaces.

A simplified architecture of the solution is shown below

![powerbi-gateway-architecture](../.img/power-bi/gateway_architecture.drawio.png)

A dataset on Databricks can be accessed from Power BI through a datasource using
the Power BI data gateway. The firewall in the cloud network have rules to allow
connections from the virtual machine running the gateway to the WDAP Databricks
workspaces and to Power BI.

## WDAP Gateways

| Gateway Name | VM(s) | User |
| --- | --- | --- |
| WindPBIGatewayClusterDevTst | sapbigd16298 | s7windpbidev |
| WindPBIGatewayClusterAccPrd | sapbigp16538, sapbigp15495 | s7windpbiprd |

## Setup Power BI Gateway

On the Power BI service, a new on-premises gateway has to be created by the
Service Admin. Current Service Admins are Gopalakrishnan Parthasarathi and
Mattias Söderholm.

### Firewall changes

The following outbound Firewall exceptions from the gateway VM have to be
requested:

| Hostname | Port |
| --- | --- |
| `*.download.microsoft.com` | 80 |
| `*.powerbi.com` | 443 |
| `*.analysis.windows.net` | 443 |
| `*.login.windows.net, login.live.com, and aadcdn.msauth.net` | 443 |
| `*.servicebus.windows.net` | 443|
| `*.servicebus.windows.net` | 5671-5672 |
| `*.servicebus.windows.net` | 9350-9354 |
| `*.frontend.clouddatahub.net` | 443 |
| `*.core.windows.net` | 443 |
| `login.microsoftonline.com` | 443 |
| `*.msftncsi.com` | 80 |
| `*.microsoftonline-p.com` | 443 |
| `*.dc.services.visualstudio.com` | 443 |

### Configure Gateway

Log on to the VM using Delinea with your a2 account and install the PowerBI
gateway client. When asked to provide the email address to use with the gateway,
provide the s7 users address (`<s7-user-name>@corp.eur.vattenfall.com`) and
select to use the default browser under 'Sign in options'. You will then be
asked to login with the s7 user in a separate browser window.

To attatch the VM to the existing gateway, you need to provide the gateway
recovery key. The recovery key is stored in the `vap2-<dev/prd>-winddata-cmn-kv`
key vaults.
