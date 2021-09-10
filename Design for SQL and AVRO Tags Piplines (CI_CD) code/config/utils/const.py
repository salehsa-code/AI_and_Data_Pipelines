
# Here are set some constants


"""
File format of files to be imported to a databrciks notebook.
"""
file_format = {'PYTHON': 'py', 'SCALA': 'scala', 'R': 'r', 'SQL': 'sql'}

"""
Here is the packaging format used to replicate the libraries in a cluster.
As of today we only support pip and conda pip dependencies.
"""
package_format = {'conda': '*.yml', 'pip': '*.txt'}
