# Access Management Naming Patterns

## Purpose

Adhering to specific naming patterns is crucial for maintaining order and consistency, which in turn facilitates efficient management and identification of resources.

However, it's important to note that Cloud Service Portal (CSP) and Local Active Directory (AD) follow different standards. CSP is used to modify Azure Active Directory (AAD) groups.

## Omada Naming

In Omada this naming standard is used for groups used in Azure:
`z_azu_[desc_][desc_][desc_][_mode]`

E.g.: `z_azu_conti_onlin_b2c__r`

## CSP Naming

In CSP this naming standard is used:
`z_[cloud-provider]_[envgroup_][env_][desc]__[mode]`

E.g.: `z_azu_vap2_accprd_acc_winddata_contrib__a`
