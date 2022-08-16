# OT Utils library

### Running S3 Copy Tool:

Running VIP Data Lake Copying Tool:
- `source_bucket`: is the name of the bucket we are going to copy FROM
- `destination_bucket`: is the name of the bucket we are going to copy TO
- `aws_access_key_id`: AWS Access Key Id
- `aws_secret_access_key`: AWS Secret Access Key


```{python}
copy_tool = VIPDataLakeCopyTool(source_bucket='s3_from',
                                destination_bucket='S3_to',
                                aws_access_key_id='1111',
                                aws_secret_access_key='XXX')
arg_date = "20220506"
prefix_path = f"{arg_date}"

# Iterate All Objects in Your S3 Bucket Over the for Loop
copy_tool.copy_buckets(prefix_path, f'poc/{prefix_path}')
```


### Running AWS Glue Tool:

Running AWS deploying Glue tool:
- `aws_access_key_id`: AWS Access Key Id
- `aws_secret_access_key`: AWS Secret Access Key
