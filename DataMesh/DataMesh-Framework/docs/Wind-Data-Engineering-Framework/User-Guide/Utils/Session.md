# Session

> Users of the Framework should not need to interact with the Session Manager.

## Overview

The Session Manager module is used to abstract the session management logic
from the rest of the framework. This abstraction allows the framework to
be tested locally without the need for a Spark cluster.

The Session Manager module is responsible for creating a Spark session and
providing it to the rest of the framework. The same is true for dbutils, which
are not available when running locally.

An environment variables `IS_DBRKS_CLUSTER` is used to track, whether
the framework is running on a Databricks cluster or locally. A spark session
is then created accordingly using databricks-connect or the local spark
installation.
