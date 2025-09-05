# Wind data and analytics platform

The Wind Data and Analytics Platform (WDAP) is an Azure cloud lakehouse and
analytics solution that supports the Wind energy business for their reporting
and analytics needs. This system receives data from several SAP and non-SAP
systems through the Vattenfall Integration Platform (VIP). The principal goal of
WDAP is to enable business users with insights that are timely as required by
the business process they feed back into. This requires that WDP be able to
develop incremental load data pipelines, provide data objects that can be
connected with each other and support building of various analytics products for
retrospective, descriptive and prescriptive analytics. The purpose of this
document is to provide a conceptual and logical architecture for WDAP.

At a high level, conceptually, the platform may be viewed as:

:::mermaid
graph LR;
    U("Consumers") --> |use| A["Wind Analytics Platform"] -->|use data from| D["Wind Data Platform"]--> |receives data from| S("Sources")
    U("Consumers") --> |use data from| D["Wind Data Platform"]
:::

## Conceptual architecture

WDAP may be conceptualized as a business service or hub that provides analytical
capabilities on top of the digital footprint of Wind business processes. WDAP
receives data from multiple producers that feed in data either from applications
or from users. On the consumption side of WDAP are three main categories of
actors:

- Business users
- Applications
- Developers/Data scientists

The Wind Data and Analytics Platform is split into two main parts:

- Data platform: The data platform provides capabilities to process and store
  data and supports near real time (down to 15 minute latency) data delivery.
  Latency is the difference in time between when a record is received by WDP to
  when it is available to different actors for use.
- Analytics platform: Different analytics products may be built using WDAP. A
  principal work load is around retrospective and descriptive analytics that
  covers reporting as well as dashboards. Based on inputs on strategic
  objectives, it is expected that over time advanced analytics products
  (including machine learning) will be built based on data in WDAP.

Within the  platform the approach needs to support the following attributes of
the architecture.

- Veracity: Trustworthiness of data brought about by lineage and integrity
- Connectedness: All data objects are connected to each other through a domain
  model.
- Explainability: Data within WDP is easy to locate and understand
- Timeliness: Data is available within acceptable periods of time that the
  business needs and aligned to a return on the right level of investment
- Maintainability: The information architecture supports easy maintenance of
  data products and the possibility to evolve the architecture over time as
  business requirements change

While data is governed, its pace of availability should not impede innovation
through analytics products. This requires the decoupling of the data products
and analytics products  as both follow different lifecycles and frequencies of
change. Whereas the data platform may have a higher initial development impetus,
it will not change much architecturally once the main components are built. The
main way the data platform will change is content coverage.

This decoupling is required for WDAP to be an engine of innovation and
facilitate rapid value creation through analytics products but at the same time
promote information governance on the data platform. A decay in the veracity of
data (the so called emergence of a data swamp) affects the analytics products
and insights that power the improvement of business processes. Therefore a
tighter data product governance is aligned to the business goals of being data
driven.

This information governance can best be achieved through establishing standards
for data modelling, coding and defining the patterns to be followed when
processing and managing data. In addition two key approaches are needed to be
followed when establishing information governance:

- Data product thinking based on domain models
- Process way of working for data onboarding
