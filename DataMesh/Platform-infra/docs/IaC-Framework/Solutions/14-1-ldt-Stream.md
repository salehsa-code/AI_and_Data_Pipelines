# LDT Stream

This is a terraform solution for the depoloyment of the LDT data stream
resources. It can be seen as an extension for an exisitng data source, hence the
name '14-1'.

The solution includes the entities on the MQTT broker (topic space, clients,
client group, permission binding), an Event Hub, where the MQTT messages are
delivered to, as well as a Namespace Topic subscription for the push delivery
towards the Event Hub and a Stream Analytics job for the event capture towards a
storage account. The stream analytics job is deployed with a system-assigned
managed identity, which is then added as a member of the Entra Id security group
to the required role assignments.

## Configuration

The solution has to be configured and deployed separately for each BU. The
configuration file is located in
`config\<env>\14_1-ldt_stream\<bu_name>\delivery.yml`. It supports the
configuration of multiple data streams. Example:

```yaml
# A map of LDT stream objects
<identifier>:                         # The key is used for terraform internal reference
  type: mqtt                          # type of the data stream. currently only mqtt
  business_unit:                      # BU name (offshore, onshore, soba)
  event_sender_group_id:              # group Id of the azure security group deployed in 10
  mqtt_topic:                         # mqtt topic configuration
    name:                             # name displayed on the Azure Portal
    templates:                        # A list of allowed MQTT topics
      - ...
  clients:                            # mqtt client config
    hkz-dev-client:                   # internal key of the client, can be the same as auth name
      authentication_name:            # auth name of the client device
      thumbprint:                     # certificate thumbprint of the client device
  event_subscription:
    event_time_to_live:               # retention time of events on the event subscription
    event_max_delivery_count:         # max delivery tries
  event_hub:                          # event hub settings
    name:                             # name of the event hub on the event hub namespace
    partition_count:                  # number of partitions
    message_retention_days:           # retention period of messages on the event hub
  streaming_job:                      # streaming job settings
    name:                             # name of the stream analytics job
    input_name:                       # name of the input data source
    output_name:                      # name of the output data source
    output_path:                      # path on the landing container on the ADLS
    streaming_units:                  # number of streaming units
    batch_min_rows:                   # minimum number of rows per batch
    batch_max_wait_time:              # maximum wait time before event delivery towards ADLS landing
    storage_container_name:           # name of the storage container
    output_format:                    # optional. output format of the data. parquet or delta. defaults to parquet
    custom_query:                     # optional. add custom query on the
    output_partition_column:          # optional. partition column
```
