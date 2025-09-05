[[_TOC_]]

#Current vs Legacy Service Principals
The default setup for new applications and associated service principals in Azure 
has the App Registration as the application object, and that application hosts the 
client secrets. It has a one to many relationship with its service principals, who 
get the secrets from the application object when they authenticate towards another 
application. More detailed information can be found in [Azure's own documentation](https://learn.microsoft.com/en-us/entra/identity-platform/app-objects-and-service-principals). 
Legacy service principals (see legacy bullet point under "Service principal object" 
heading on the same [wiki page](https://learn.microsoft.com/en-us/entra/identity-platform/app-objects-and-service-principals?tabs=browser#service-principal-object)) instead exist on their own as a standalone 
application, without an associated app registration. Secret management for these 
principals is no longer supported through the in browser Azure portal nor the Entra admin center.

#Updating credentials for Legacy Service Principals
To update credentials you need to be an owner of the application (i.e. the service 
principal) and use the Azure CLI. You also need the application ID to be able to 
update the secret. If you do not have this, you can use `az ad sp list --filter "displayName eq '<name of application>'"` 
to find it. Once you have the application ID, you can use `az ad sp credential reset --id <application ID>`. 
Documentation can be found [here](https://learn.microsoft.com/en-us/cli/azure/ad/sp/credential?view=azure-cli-latest#az-ad-sp-credential-reset).

#Editing ownership of Legacy Service Principals
This can currently still be done manually through the Azure portal. Should this change, 
or should you want it automated in a script, you can use the rest API. The simplest way 
to do this is through the Azure CLI 
`az rest --method POST --uri https://graph.microsoft.com/v1.0/servicePrincipals/<target SP Object ID>/owners/\$ref --body "{\"@odata.id\": \"https://graph.microsoft.com/v1.0/directoryObjects/<new owner Object ID>\"}"`. 
To find the object ID of a user, you can find them in the Azure portal and copy it from 
the user overview. Rest API documentation for adding owners can be found [here](https://learn.microsoft.com/en-us/graph/api/serviceprincipal-post-owners?view=graph-rest-1.0), and Azure CLI rest documentation can 
be found [here](https://learn.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest#az-rest).