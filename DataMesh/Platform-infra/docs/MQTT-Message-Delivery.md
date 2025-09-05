# Lean Data Transport (LDT) - MQTT Message Delivery

Messages broadcasted via MQTT protocol can be collected by an MQTT broker that
operates on an Event Grid Namespace. From that namespace, messages can be sent
to an Event Hub on an Event Hub Namespace using push delivery from a Event Grid
Namespace Topic on the Event Grid Namespace. From the Event Hub, the messages
can be delivered as Event Capture via an Azure Stream Analytics job to a storage
account, or made available via a Kafka Endpoint.

The current solution design forsees a **push** delivery via Azure Stream Analytics
towards a storage account in the landing area of a WDAP data source. The Stream
Analytics Jobs authenticate using their system-assigned managed identity. To
distribute the required access on the storage account and event hub namespace,
the managed identites are added to an Entra Id security group with the required
role assignments.

Below drawing illustrates the design of the MQTT message delivery.

![mqtt-delivery-design](.img/event-grid/mqtt-streaming.drawio.png)

## Infrastructure

### BU Specific Setups

For each BU (Onshore, Offshore, SoBa), separate Azure Resource Groups are
deployed with the above described infrastructure to separate workloads for
clearer cost allocation. The naming convention follows the pattern
`vap2-<env>-wdap-ldt-<bu>-we-rg`, where `env` referes to the project environment
(`dev` for development or `prd` production) and `bu` specifies the BU (`off` for
offshore, `on` for onshore, `soba` for SoBa).

Each deployment is configured and managed separately using the [WDAP IaC
Framework](IaC-Framework.md). The section below details the exact process and
describes the configurations neccessary.

### Implementation in IaC

The solution is split into three separate deployments on the IaC framework:

- Entra Id Groups
- Core infrastructure
- Data stream infrastructure

For the configuration of these solutions, refere to the
[11-1](IaC-Framework/Solutions/11-1-LDT-Infra.md#configuration) and
[14-1](IaC-Framework/Solutions/14-1-ldt-Stream.md#configuration) sections in the
documentation of the IaC Framework.

The Entra Id security groups used to distrubute access to the event hub
namespaces and storage account are deployed in the `10-platform_automation_core`
solution.

The core infrastructure consists of an Event Grid Namespace with Event Grid
Namespace topic used to collect all incomming MQTT messages and an Event Hub
Namespace, where the Event Hubs for the message delivery are deployed to. This
solution also deploys the User Managed Identity used for the push delivery from
the event grid namespace to the event hubs on the event hub namespace. These
resources are deployed as part of the `11_1-ldt_infra` solution.

The data stream infrastructure includes the entities on the MQTT broker (topic
space, clients, client group, permission binding), an Event Hub, where the MQTT
messages are delivered to, as well as a Namespace Topic subscription for the
push delivery towards the Event Hub and a Stream Analytics job for the event
capture towards a storage account. The stream analytics job is deployed with a
system-assigned managed identity, which is then added as a member of the Entra
Id security group to the required role assignments. These resources are deployed
as part of the `14_1-ldt_stream` solution.

#### Manual steps after deployment

Since the Event Grid Namespace with MQTT capabilites is currently unavailable as
a Terraform resource, it is deployed using the AzAPI provider which comes with
less flexibility compared to an actual Terraform resource and requires some
additional manual steps after deployment.

The MQTT broker needs to be enabled on the Event Grid Namespace after deployment
in the Azure Portal in the "Configuration" blade of the Event Grid Namespace
resource. This process takes a few minutes and cannot be reverted once it is
enabled. Additionally, the MQTT message routing towards the Event Grid Namespace
topic must be configured in the "Routing" blade of the Event Grid Namespace
resource. Choose "Namespace topic" as topic type and the topic that was deployed
for the Event Grid Namespace under topic. Additionally, specify the
`clienttopic` and `mqtttopic` keys under Message Enrichments as follows:

| Key | Type | Value |
| --- | --- | --- |
|`clienttopic` | Dynamic | `${client.attributes.topic_name}` |

The Azure Stream Analytics job is paused after the initial deployment and needs
to be started, once messages are arriving on the Event Hub.

### Client Authentication

The MQTT broker on the event grid namespace supports two types of
authentication, certificate based or (only for MQTT v5) Entra Id based
authentication via RBAC assignments.

Using certificate based authentication, there is either the option to verify the
certificate thumbprint (SHA1-checksum) or validate the client via a CA
certificate.

#### Authentication using CA certificate chain

For CA certificate chain based authentication, the root or intermediate
certificate used to sign the client certificate has to be uploaded to the
eventgrid namespace MQTT broker. This can be done on the Azure portal via the
"CA Certificates" blade under the MQTT broker panel on the event grid namespace.

The client on the MQTT broker must be configured with "Subject Matches
Authenticaion Name" as Client Certificate Authentication Validation Scheme. In
the client certificate subject, the common name (CN) must match the clients
authentication name configured on the MQTT broker. To verify this, you can use
the following command on the client certificate, which will print the
certificate information to the console:

```console
$ openssl x509 -text -in <path/to/client.crt>
Certificate:
    Data:
        [ ... ]
        Subject: CN = <client-auth-name>
        [ ... ]
```

##### Example to create a CA chain

The following code shows how to create a self-signed root CA certificate and
derive client certificates from it:

```bash
CLIENT="test-client" # authentication name of your client

mkdir -p certs
cd ./certs

if [ ! -f "./rootCA.key" ]; then
  # Create root CA & Private key
  openssl req -x509 \
              -sha256 -days 356 \
              -nodes \
              -newkey rsa:2048 \
              -subj "/CN=afh-test-root-CA" \
              -keyout rootCA.key -out rootCA.crt
fi

# Generate Private key
openssl genrsa -out ${CLIENT}.key 2048

# Create CSR request using private key
openssl req -new -key ${CLIENT}.key -out ${CLIENT}.csr -subj "/CN=${CLIENT}" \

# Create SSl with self-signed CA
openssl x509 -req \
    -in ${CLIENT}.csr \
    -CA rootCA.crt -CAkey rootCA.key \
    -CAcreateserial -out ${CLIENT}.crt \
    -days 365 \
    -subj "/CN=${CLIENT}" \
    -sha256

# Clen-up
rm ${CLIENT}.csr
```

The script creates a new folder called `certs`, within it you find the root CA
certificate and a client certificate. The root CA certificate needs to be added
to the MQTT broker on the eventgrid namespace and then the client certificate
can be used to authenticate to the MQTT broker.

## Processing of Messages

### SparkplugB

Messages via LDT will arive following the SparkplugB standard. That means we
will receive messages that contain multiple measurements / tags and need to be
unpacked.

In WDAP the unpacking is handled using the WinDEF. A code snippet
sketching how the unpacking is done is shown below:

```python
df = spark.read.format("delta").load("path/to/table/with/sparkplug.delta")
# assume message is a column storing a complex object with field "metrics"
# containing an array of metrics / tags
df_unpacked = df.withColumn("metric", explode("message.metrics"))
```

### Protobuf

Messages via LDT can additionally be encoded using Protobuf. The protobuf needs
to be decoded using a protobuf schema before it can be further processed. To
decode the protobuf schema descritor file needs to be provided.

To create a protobuf descriptor file from a protobuf schema use:

```sh
protoc --include_imports --descriptor_set_out=<filename>.desc <filename>.prot
```

Protobuf decoding can be done natively in pyspark. In WDAP the decoding is
handled using WinDEF. The following code snippet highlights how the decoding is
done:

```python
df = spark.read.format("delta").load("path/to/table/with/sparkplug.delta")
# assume message is a column containing the message encoded with protobuf.
df_decoded = df_unbase.withColumn(
    "decoded",
    from_protobuf(
        col("message"),
        descFilePath="/Volumes/vap2_dev_wdap_sources/ot_mqtt/config/protobuf_descriptors/sparkplug_b.desc",
        messageName="Payload",
        options={"recursive.fields.max.depth": 2},
    ),
)
df_unpacked.withColumn("metric", explode("decoded.metrics"))
```
