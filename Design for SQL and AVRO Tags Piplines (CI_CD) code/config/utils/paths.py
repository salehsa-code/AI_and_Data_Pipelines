def create_full_target_path(root_dir, rest_of_path, source_notebook_dir, target_notebook_dir, drop_extensions=False):
    """
    This util function takes in a path on a source system, and readies it for Databricks linux-baesd FS

    :param root_dir:
    :param rest_of_path:
    :param source_notebook_dir:
    :param target_notebook_dir:
    :param drop_extensions: If we are handling a notebook (as opposed to a DIR), we must drop the extension on import
    :return:
    """
    # handle Windows Paths on source_notebook_dir incase ingesting from windows machine
    new_root = root_dir.replace(source_notebook_dir, target_notebook_dir).replace('\\', '/') + '/'

    if drop_extensions:
        rest_of_path = rest_of_path.rstrip(".sql")

    print("create_full_target_path(): Returning {}".format(new_root + rest_of_path))
    return new_root + rest_of_path