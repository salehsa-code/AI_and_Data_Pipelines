import ntpath
import os
import typing
from datetime import datetime
from pathlib import Path, WindowsPath

import boto3


class S3CopyingTool:

    def __init__(self,
                 source_bucket: str,
                 destination_bucket: str,
                 aws_access_key_id: str,
                 aws_secret_access_key: str,
                 retries: int = 3):
        self.session = boto3.Session(aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key)

        self.s3 = self.session.resource('s3', verify=False)

        self.source_bucket = self.s3.Bucket(source_bucket)
        self.destination_bucket = self.s3.Bucket(destination_bucket)

        self.retries = retries

    @staticmethod
    def _get_list_files(bucket, prefix: str) -> typing.Dict:
        list_files = [Path(s3_file.key) for s3_file in bucket.objects.filter(Prefix=prefix)]
        file_dict = {}
        for s3_file in list_files:
            file_dict[s3_file.name] = s3_file
        return file_dict

    @property
    def folder_to_scan(self) -> str:
        NotImplementedError("folder_to_scan must be implemented")

    def _intersection(self, dict1, dict2) -> typing.Dict:
        intersection_dict = {}
        for value in dict1.keys():
            if self._create_copied_name(dict1[value]) not in dict2.keys():
                intersection_dict[value] = dict1[value]
        return intersection_dict

    def _intersection_buckets(self, source_prefix: str, destination_prefix: str) -> typing.Dict:
        source_dict = self._get_list_files(self.source_bucket, source_prefix)
        destination_dict = self._get_list_files(self.destination_bucket, destination_prefix)
        return self._intersection(source_dict, destination_dict)

    @staticmethod
    def _make_destination_path(original_path: Path, destination_path: Path) -> Path:
        build_path = ""
        for folder_o in original_path.parts[::-1]:
            if folder_o in destination_path.parts:
                return Path(f"{destination_path.resolve()}{os.sep}{build_path}")
            if folder_o is not original_path.name:
                build_path = f"{folder_o}{os.sep}{build_path}"
        return destination_path

    def _copy_buckets_intersection(self, intersection_dict: typing.Dict, destination_prefix: str):
        destination_path = Path(destination_prefix)
        for s3_file in intersection_dict.keys():
            copy_source = {
                'Bucket': self.source_bucket.name,
                'Key': intersection_dict[s3_file].resolve()
            }
            filename = self._create_copied_name(intersection_dict[s3_file])
            destination_file_path = self._make_destination_path(intersection_dict[s3_file], destination_path)
            destination_file_path = f"{ destination_file_path}{os.sep}{filename}"
            print(destination_file_path)
            # self.destination_bucket.copy(copy_source, destination_file_path)
            # print(s3_file + '- File Copied')

    @staticmethod
    def _create_copied_name(file_name: Path) -> str:
        date_input_format = "%Y%m%d"
        datetime_output_format = "%Y%m%dT%H%M%S"
        day_time = datetime.strptime(file_name.parent.parent.name, date_input_format).replace(
            hour=int(file_name.parent.name))
        datetime_str = day_time.strftime(datetime_output_format)
        return f"{file_name.stem}_{datetime_str}{''.join(file_name.suffixes)}"

    def copy_buckets(self, run_date: str, destination_prefix: str):
        source_prefix = f"{self.folder_to_scan}{os.sep}{run_date}"
        intersection_dict = self._intersection_buckets(source_prefix=source_prefix,
                                                       destination_prefix=destination_prefix)
        while self.retries > 0 and len(intersection_dict) > 0:
            self._copy_buckets_intersection(intersection_dict=intersection_dict,
                                            destination_prefix=destination_prefix)
            self.retries -= 1
