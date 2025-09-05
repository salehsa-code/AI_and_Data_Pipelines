# LDT Core Infrastructure

This solution deploys the infrastructure for MQTT streaming usecases, this
includes an Eventgrid Namespace with an Event Topic for MQTT message delivery and
Event Hub Namespace. The solution can be deployed for multiple instances. It is
forseen that one instance is deployed per BU.

## Deployment

After the initial deployment, the MQTT broker Eventgrid Namespace must be
manually activated, because this functionality is currently unavailable via the
Azure Resource Manager. It can be activated via the Azure Portal on the
Eventgrid Namespace resource under the `configuration` blade. For the event
delivery, the event-delivery managed identity requires the `Azure Event Hubs
Data Owner` role on the Event Hub Namespace. Additionally the LDT group for the
given BU must get the `Azure Event Hubs Data Receiver` role on the Event Hub
Namespace and the `Storage Blob Data Contributor` role on the data sources
storage account.

## Configuration

The solution has to be configured and deployed separately for each BU, if a use
case requires the LDT infrastructure. The configuration files are located in
`config/<env>/11_1-ldt_infra/<bu_name>`. There is also a
`config/<env>/11_1-ldt_infra/global.yml` config file that contains general
config parameters:

```yaml
resource_groups:
  winddata: "vap2-dev-winddata-we-rg" # name of the WDAP resource group
  ldt: "vap2-dev-wdap-ldt-off-we-rg"  # name of the LDT resource group
user_assigned_identities:
  event_delivery:
    name: vap2-dev-wdap-ldt-off-delivery-uami # name of the event delivery managed identity
    resource_group: ldt # key of the resource group where the MI is deployed
```

The `event.yml` config file contains config parameters for the event hub and
event grid namespace resources:

```yaml
eventgrid:
    name:                       # name of the event grid namespace
    resource_group: ldt         # resource group key where the event grid namespace is deployed (see global.yml)
    tags: {}                    # additional tags to be added to the event grid namespace
    is_zone_redundant: false    # zone redundancy settings. keep as false, unless you know what you do.
    capacity:                   # capacity of the event grid namespace (between 1 and 20)
    namespace_topic_name:       # event grid topic name where messages are delivered to
    namespace_topic_retention:  # retention period of messages in days
    ip_rules: []                # ip access rules, currently not supported from OT site
eventhub_namespace:
    name:                       # name of the event hub namespace
    resource_group: ldt         # resource group key where the event hub namespace is deployed (see global.yml)
    sku: Standard               # SKU of the event hub namespace
    capacity:                   # capacity of the event hub namespace (between 1 and 20)
    tags: {}                    # additional tags to be added to the event hub namespace
    # below are parameters regarding network settings, which are not yet supported from OT site.
    public_network_access_enabled: true
    default_action: Allow
    trusted_service_access_enabled: true
    ip_rules: []
    allowed_subnets: []
```
