
# Common Lib framework adding external Lib guide

 This guide is intended for platfrom team / SD to enable the external lib usage
 into WDAP platfrom via jFrog cloud.

## Developer Guidelines

This section is explaning the process to be followed to enable external repo
access via jFrog cloud

### Solutions

Request can be sent to **container services team** via **ITSP** or **Remedy**
with below information to open the firewall and enable the external repo access
via jFrog cloud

- AAD that group contains the S7 user to access the jFrog cloud artifact.
- SLA
- external repository URL
- booking element

*Turn arround time will be in a day or two.*

*Effort min 1 hour or max 8 hours depending on the current setup in the VCS and
the external repo list (the VCS team needs some time to open the firewall
request and for further alignment with VDPs network team to enable access to the
repos from the jFrog artifactory.)*

*Security compliance:* Projects are responsible. Platform Team makes sure that
BISO approval has been in place before any external lib is getting used in the
environment.

*BISO contact:* Alexander Papitsch
