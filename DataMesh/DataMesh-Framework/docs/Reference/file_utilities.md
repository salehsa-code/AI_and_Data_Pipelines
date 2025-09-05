# Table of Contents

* [generate\_random\_csv](#generate_random_csv)
* [get\_file\_paths](#get_file_paths)
* [get\_file\_paths.factory](#get_file_paths.factory)
* [get\_file\_paths.exceptions](#get_file_paths.exceptions)
* [get\_file\_paths.location\_types](#get_file_paths.location_types)
* [get\_file\_paths.get\_file\_paths](#get_file_paths.get_file_paths)
* [get\_file\_paths.strategies.base\_strategy](#get_file_paths.strategies.base_strategy)
* [get\_file\_paths.strategies](#get_file_paths.strategies)
* [get\_file\_paths.strategies.utils\_strategy](#get_file_paths.strategies.utils_strategy)
* [get\_file\_paths.strategies.local\_strategy](#get_file_paths.strategies.local_strategy)

<h1 id="generate_random_csv">generate_random_csv</h1>

<h4 id="generate_random_csv.create_csv">create_csv</h4>

```python
def create_csv(base_name, num_files, num_rows, names, types)
```

Generates multiple CSV files with random data.

This function creates a specified number of CSV files, each containing a specified number of rows with
random data. The names and types of the columns in the CSV files are also specified by the user.

**Arguments**:

- `base_name` _str_ - The base name for the CSV files. The actual file name will be formed by appending an
  underscore and the file index to the base name.
- `num_files` _int_ - The number of CSV files to create.
- `num_rows` _int_ - The number of rows of data in each CSV file.
- `names` _list[str]_ - A list of strings specifying the names of the columns in the CSV files.
- `types` _list[str]_ - A list of strings specifying the types of the columns in the CSV files.
  The supported types are 'id', 'partition', 'int', 'float', 'float_positive', 'float_normal_0',
  'string', and 'email'.
  

**Raises**:

- `ValueError` - If an unsupported column type is specified.
  
  Writes:
  CSV files with the specified base name, each containing the specified number of rows of random data.
  The files are written in the current working directory.
  

**Example**:

```python
create_csv("test_data", 10, 100, ["id", "name", "email"], ["id", "string", "email"])
```

<h1 id="get_file_paths">get_file_paths</h1>

<h1 id="get_file_paths.factory">get_file_paths.factory</h1>

<h2 id="get_file_paths.factory.FileRetrievalFactory">FileRetrievalFactory</h2>

```python
class FileRetrievalFactory()
```

Factory for creating file retrieval strategies based on location type.

This factory class is responsible for returning the appropriate strategy
implementation for retrieving files based on the specified location type.

<h4 id="get_file_paths.factory.FileRetrievalFactory.get_strategy">get_strategy</h4>

```python
@staticmethod
def get_strategy(location_type: LocationType) -> FileRetrievalStrategy
```

Returns the appropriate file retrieval strategy for the given location type.

Depending on the provided location type, this method returns an instance
of either `LocalDirectoryStrategy` or `UtilsStrategy`. If the
location type is not recognized, a `ValueError` is raised.

**Arguments**:

- `location_type` - The location type for which to get the retrieval strategy.
  

**Returns**:

- `FileRetrievalStrategy` - An instance of the appropriate file retrieval strategy.
  

**Raises**:

- `ValueError` - If the provided location type is unknown or unsupported.

<h1 id="get_file_paths.exceptions">get_file_paths.exceptions</h1>

<h2 id="get_file_paths.exceptions.FileUtilitiesError">FileUtilitiesError</h2>

```python
class FileUtilitiesError(Exception)
```

Base class for file utility exceptions.

<h1 id="get_file_paths.location_types">get_file_paths.location_types</h1>

<h2 id="get_file_paths.location_types.LocationType">LocationType</h2>

```python
class LocationType(Enum)
```

Enum representing different types of locations.

**Attributes**:

- `LOCAL` - Represents a local location.
- `VOLUME` - Represents a volume location.
- `ABFS` - Represents an Azure Blob File System (ABFS) location.

<h4 id="get_file_paths.location_types.LocationType.list">list</h4>

```python
@staticmethod
def list() -> list[str]
```

Returns a list of all location type values.

This method provides a list of strings, each representing a location type.

**Returns**:

  list of str: A list of all the values of the LocationType enum.

<h1 id="get_file_paths.get_file_paths">get_file_paths.get_file_paths</h1>

<h4 id="get_file_paths.get_file_paths.get_file_paths">get_file_paths</h4>

```python
def get_file_paths(location: str,
                   file_name_pattern: str | None = None,
                   search_subdirs: bool = True) -> list[str]
```

Retrieves file paths from a specified location based on the provided criteria.

This function determines the type of location (e.g., local directory, blob storage),
retrieves the appropriate file retrieval strategy using a factory, and then uses
that strategy to get a list of file paths that match the given file_name_pattern and search options.

**Arguments**:

- `location` - The location to search for files. This could be a path to a local directory or a URI for blob storage.
- `file_name_pattern` - The file file_name_pattern to filter by as string. None retrieves all files regardless of file_name_pattern.
- `search_subdirs` - Whether to include files from subdirectories in the search.
  

**Returns**:

  A list of file paths that match the specified criteria. The paths are returned as strings.
  

**Raises**:

- `ValueError` - If the `location` argument is empty or None.
- `FileUtilitiesError` - If an error occurs while determining the location type, retrieving the strategy, or getting file paths.

<h4 id="get_file_paths.get_file_paths.get_location_type">get_location_type</h4>

```python
def get_location_type(location: str) -> LocationType
```

Get the location type based on the given location string.

**Arguments**:

- `location` - The location string to check.
  

**Returns**:

- `LocationType` - The determined location type.

<h1 id="get_file_paths.strategies.base_strategy">get_file_paths.strategies.base_strategy</h1>

<h2 id="get_file_paths.strategies.base_strategy.FileRetrievalStrategy">FileRetrievalStrategy</h2>

```python
class FileRetrievalStrategy(ABC)
```

Abstract base class for file retrieval strategies.

This class defines the interface for strategies that retrieve file paths
based on certain criteria. Concrete implementations of this class should
provide the logic for retrieving file paths.

<h4 id="get_file_paths.strategies.base_strategy.FileRetrievalStrategy.get_file_paths">get_file_paths</h4>

```python
@staticmethod
@abstractmethod
def get_file_paths(location: str,
                   file_name_pattern: str | None = None,
                   search_subdirs: bool = True) -> list[str]
```

Retrieves a list of file paths based on the specified criteria.

**Arguments**:

- `location` - The location to search for files.
- `file_name_pattern` - The file file_name_pattern to filter by. If None, no file_name_pattern filtering is applied.
- `search_subdirs` - Whether to search in subdirectories.
  

**Returns**:

- `list[str]` - A list of file paths that match the specified criteria.

<h1 id="get_file_paths.strategies">get_file_paths.strategies</h1>

<h1 id="get_file_paths.strategies.utils_strategy">get_file_paths.strategies.utils_strategy</h1>

<h2 id="get_file_paths.strategies.utils_strategy.UtilsStrategy">UtilsStrategy</h2>

```python
class UtilsStrategy(FileRetrievalStrategy)
```

Strategy for retrieving files using DButils (in Databricks) and mssparkutils (in Fabric).

This strategy implements the file retrieval logic using utils, including
recursive search through directories and filtering by file file_name_pattern.

<h4 id="get_file_paths.strategies.utils_strategy.UtilsStrategy.get_file_paths">get_file_paths</h4>

```python
@staticmethod
def get_file_paths(location: str,
                   file_name_pattern: str | None = None,
                   search_subdirs: bool = True) -> list
```

Recursively retrieves all files with a specified file_name_pattern from a given directory and its subdirectories.

**Arguments**:

- `location` - Top-level directory to read from, e.g., '/Volumes/my_volume/landing/example_landing/'.
- `file_name_pattern` - File file_name_pattern, None to get all files.
  
- `search_subdirs` - If True, function will also search within all subdirectories.
  

**Returns**:

- `List` - List of files in the directory and its subdirectories with the given file_name_pattern.
  

**Raises**:

- `ValueError` - If the location is not provided.
- `Exception` - For any other unexpected errors.

<h1 id="get_file_paths.strategies.local_strategy">get_file_paths.strategies.local_strategy</h1>

<h2 id="get_file_paths.strategies.local_strategy.LocalDirectoryStrategy">LocalDirectoryStrategy</h2>

```python
class LocalDirectoryStrategy(FileRetrievalStrategy)
```

Strategy for retrieving files from a local directory.

This strategy implements the file retrieval logic for local directories, including
optional recursive search through subdirectories and filtering by file file_name_pattern.

<h4 id="get_file_paths.strategies.local_strategy.LocalDirectoryStrategy.get_file_paths">get_file_paths</h4>

```python
@staticmethod
def get_file_paths(location: str,
                   file_name_pattern: str | None = None,
                   search_subdirs: bool = True) -> list[str]
```

Recursively retrieves all files with a specified file_name_pattern from a given directory and its subdirectories.

**Arguments**:

- `location` - Top-level directory to read from, e.g., '/Volumes/my_volume/landing/example_landing/'.
- `file_name_pattern` - File file_name_pattern, None to get all files.
- `search_subdirs` - If True, function will also search within all subdirectories.
  

**Returns**:

- `List` - List of files in the directory and its subdirectories with the given file_name_pattern.
  

**Raises**:

- `ValueError` - If the location is not provided.
- `FileUtilitiesError` - For any other unexpected errors.

