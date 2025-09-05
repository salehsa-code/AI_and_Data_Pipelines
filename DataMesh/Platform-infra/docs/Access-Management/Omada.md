# Omada

## Content

[[_TOC_]]

## Purpose

Omada is primarily used for the WDAP Access Management due to its comprehensive
IAM capabilities. It is equipped to manage all access-related processes,
including access requests, review, approval, denial, role definition, and
resource mapping. Whenever possible, Omada should be used over other solutions
(such as CSP).

## Limitations of Omada

Omada only processes requests for Active Directory (AD), not Azure Active
Directory. As a result, it cannot manage requests for Service Principals and a7
accounts, as these are not recognized in the local AD.

## Omada User Requests

<!-- This works in the Azure DevOps Wiki, but not locally -->
![Process for users to request Access via Omada](../.img/access-management/omada-user-flow.png =500x)

1. VF Employees access Omada with their browser at iam/.
2. Access to resources can be requested in IAM.
3. Resources are mapped to AD groups. AD groups have access to Resources as a specific role.
4. AD groups are synced to Azure AD.
5. AAD groups have access to Azure resources (e.g., Resource Groups).
6. Users with assignments to appropriate (A)AD groups can access resources.

### How-To Request Access in Omada

1. Go to `iam` in the Edge browser
1. Select `Services` → `Request Access`
1. Specify `WDAP` as system and search for the role
1. On the desired role click `Add`  (repeat this step if multiple roles are required)

![Image showing how to Order an Omada Role](../.img/access-management/OmadaSearch.png =x400)

1. In the bottom right click `Submit` (This looks like Cookie consent!)

### How-To Grant Access in Omada

1. When a user requests access to a role, that you own, you will get an email with a subject like
`[Action required] You have been assigned an IAM task: "Approve requested access"`
1. Either follow the link in that mail or manually go to `iam` in the Edge browser
1. On the landing page you will be prompted with `TASKS` - `Approval of the resource manager`
1. Open your tasks
1. Review all open access requests and set the radio button on the right to `approved` or `rejected`
   - You can review the details to see the mandatory reason, that was provided by the requestor

![Image showing how to Review a request in Omada](../.img/access-management/OmadaReviewRequest.png =x150)

1. In the bottom right click `Submit` (This looks like Cookie consent!)

> Apparently the requestor does not get notified, when access has been granted. Therefore it might be helpful
> to manually inform the person.

### How-To Revoke Access in Omada

1. Go to `iam` in the Edge browser
1. Go to `My Data` → `My Resources`
1. Search for the Resource you want to revoke access to
1. Select that resource and in the details page select `Assignments` (Yellow button in the top)
1. Tick the checkbox for users you want to revoke access for and click `Expire` and confirm

> Apparently the user does not get notified, when access has been revoked. Therefore it might be helpful
> to manually inform the person.

### How-To Review Access in Omada

To review the access of users, follow the same steps as in the [Revoking section](#how-to-revoke-access-in-omada),
without expiring the access.

## Omada Roles

Currently (2024-04-03) these roles are implemented:

| Role Name                             | Environments       | Mapped (A)AD groups                                                                               |
| ------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------- |
| **Data Engineer**                     | DEV, TST, ACC, PRD | z_azu_vap2_[envgroup]\_[env]\_wind_engineer_a <br>z_azu_vap2_[envgroup]\_[env]\_wind_reader__a    |
| **Data Scientist**                    | DEV, TST, ACC, PRD | z_azu_vap2_[envgroup]\_[env]\_wind_datascience_a <br>z_azu_vap2_[envgroup]\_[env]\_wind_reader__a |
| **Data Analyst**                      | DEV, TST, ACC, PRD | z_azu_vap2_[envgroup]\_[env]\_wind_bianalyst_a <br>z_azu_vap2_[envgroup]\_[env]\_wind_reader__a   |
| **Lubrication Analytics Reader**      | DEV, TST, ACC, PRD | z_azu_vap2_[envgroup]\_[env]\_lubric_analytics__r                                                 |
| **Lubrication Analytics Contributor** | DEV, TST, ACC, PRD | z_azu_vap2_[envgroup]\_[env]\_lubric_analytics__a                                                 |
| **Adept Engineer**                    | DEV, TST, ACC, PRD | z_azu_vap2_[envgroup]\_[env]\_wind_adept__a                                                       |
| **WAI Engineer**                      | DEV, TST, ACC, PRD | z_azu_vap2_[envgroup]\_[env]\_wind_wai__a                                                         |
| **Wizards Engineer**                  | DEV, TST, ACC, PRD | z_azu_vap2_[envgroup]\_[env]\_wind_wizards__a                                                     |
| **Pilots Engineer**                   | DEV, TST, ACC, PRD | z_azu_vap2_[envgroup]\_[env]\_wind_pilots__a                                                      |
