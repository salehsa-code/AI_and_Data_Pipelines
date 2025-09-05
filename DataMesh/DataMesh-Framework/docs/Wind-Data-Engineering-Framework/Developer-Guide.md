# Developer Guide

## How to contribute

Contribution to the framework is highly appreciated. It's main purpose is to
integrate knowledge of all teams into a single framework that helps everyone
with his or her work.

If you have developed a feature that you want to share with use users of the
framework, you start with checking out the main branch of the frameworks
repository. Then you create a feature branch and add your code. Please make sure
that the name of your feature branch star a meainingful name like `feature/`

For changes to the Python package, you can build the package from your feature
branch and make it available from the local PyPI. It will include a "b" for
"beta" in it's package version. (Check out
[PEP440](https://peps.python.org/pep-0440/) for more information on how to mark
pre-release version of packages.) You can then install and test it on a
Databricks cluster.

Besides making sure that your code works as expected, you should also ensure the
you fulfil the requirements of the _Definition of Done_ below. They ensure a
minimum level of quality.

When you are happy with your changes, you create a pull request in Azure DevOps.
Someone from the responsible team will review your code and either approve
directly or come back with feedback. Thank you for contributing!

::: mermaid
  graph LR;
    A[Clone repo and \n checkout main] --> B[Create Feature branch]
    B --> C[Build, Deploy, Test]
    C --> C
    C --> D[Create Pull Request]
:::

## Definition of Done

- PEP8 is followed
- Unit tests exist where sensible
- Unit tests succeed
- Changes are documented
- Code is documented

## Versioning

Versions are created in the format `major.minor.patch`. Versioning is based on
Tags in Azure DevOps. When a new version is created, the major, minor and patch
version are updated accordingly and a Tag in the repository is created. All
developments in feature branches will then be released as
`<major>.<minor>.<patch>.beta`. Once a PR to the main branch is completed, the
version will be released as `<major>.<minor>.<patch>`. This has do be done
manually by running the Azure Pipeline with the `is_beta` parameter set to
`False`.

> The version in `pyproject.toml` is not used for versioning, but it cannot be
> empty and is therefore set to 0.0.0.

So for a new version, the following steps are required:

1. Create a new Tag in Azure DevOps (where `new_patch` would ideally be 0)

    ```bash
    git tag <new_major>.<new_minor>.<new_patch>
    git push origin --tags
    ```

2. Create a new feature branch & develop your feature
    - The versions for the package from the feature branch will be
      `<new_major>.<new_minor>.<new_patch>.beta`
3. Merge your feature branch into the main branch
4. Manually run the Azure Pipeline with the `is_beta` parameter set to `False`
    - The versions for the package from the main branch will be
      `<new_major>.<new_minor>.<new_patch>`
