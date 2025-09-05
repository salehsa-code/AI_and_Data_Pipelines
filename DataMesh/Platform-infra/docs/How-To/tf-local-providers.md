# Installing provides without network access

You can install providers from local directories. The easiest way is to copy them to the [Implied Local Mirror Directories](https://developer.hashicorp.com/terraform/cli/config/config-file#implied-local-mirror-directories):

- Windows: `%APPDATA%/terraform.d/plugins and
  %APPDATA%/HashiCorp/Terraform/plugins`
- Linux: `$HOME/.terraform.d/plugins` and `terraform/plugins` located within a
  valid XDG Base Directory data directory such as
  `$XDG_DATA_HOME/terraform/plugins`. Without any XDG environment variables set,
  Terraform will use `~/.local/share/terraform/plugins`,
  `/usr/local/share/terraform/plugins`, and `/usr/share/terraform/plugins`.

If you start developing your Terraform code on a machine with network access,
then you can use `terraform providers mirror` to download the required providers
for the current configuration
([Documentation](https://developer.hashicorp.com/terraform/cli/commands/providers/mirror#command-terraform-providers-mirror)).
