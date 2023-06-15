from palanystorage.schema import StorageConfigSchema, StoredObject, WriteProgressSchema
import oss2
from typing import Union, Callable
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import os
import traceback
from palanystorage.exceptions import WriteFileFailed, HeadFileFailed
from qcloud_cos.cos_client import CosServiceError


class PalTxcosDialect:
    driver = 'pal_txcos'

    def __init__(self, storage_config: StorageConfigSchema):
        self.storage_config = storage_config
        _config = CosConfig(
            Region=self.storage_config.region,
            SecretId=self.storage_config.access_key,
            SecretKey=self.storage_config.access_key_secret,
            Token=None,
            Scheme='https')
        self.client = CosS3Client(_config)
        self.bucket_name = self.storage_config.bucket

    async def ready(self, **kwargs):
        pass

    def write_progress_maker(self, wrote_bytes: int, total_bytes: int, **kwargs) -> WriteProgressSchema:
        return WriteProgressSchema(wrote_bytes=wrote_bytes, total_bytes=total_bytes)

    async def write_file(self,
                         file_path: str,
                         key: str,
                         progress_callback: Union[Callable] = None, **kwargs):
        """
        Write File
        :param file_path:
        :param key:
        :param progress_callback:
        :param kwargs:
        :return:
        """

        try:
            res = self.client.upload_file(
                Bucket=self.bucket_name,
                LocalFilePath=file_path,
                Key=key,
                PartSize=1,
                MAXThread=3,
                EnableMD5=False
            )
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            raise WriteFileFailed(eid=WriteFileFailed.Eid.storage_upload_failed)

        return StoredObject(
            storage_id=self.storage_config.storage_id,
            key=key,
        )

    async def read_file(self, key: str, **kwargs):
        """
        Read File
        :param key:
        :param kwargs:
        :return:
        """
        pass

    async def meta_file(self, key: str, expires: int, **kwargs) -> StoredObject:
        """
        Meta file
        :param key:
        :param kwargs:
        :return:
        """

        fname = key.split(os.sep)[-1]
        url = self.client.get_presigned_url(
            Method='GET',
            Bucket=self.bucket_name,
            Key=key,
            Params={
                'response-content-disposition': f'attachment; filename={fname}'  # 下载时保存为指定的文件
                # 除了 response-content-disposition，还支持 response-cache-control、response-content-encoding、response-content-language、
                # response-content-type、response-expires 等请求参数，详见下载对象 API，https://cloud.tencent.com/document/product/436/7753
            },
            Expired=expires  # 120秒后过期，过期时间请根据自身场景定义
        )

        return StoredObject(
            storage_id=self.storage_config.storage_id,
            key=key,
            url=url,
        )

    async def delete_file(self, key: str, **kwargs) -> str:
        res = self.client.delete_objects([key,])
        return res.get('Deleted', [])[0]

    async def delete_files(self, keys: list[str], **kwargs) -> list[str]:

        res = self.client.delete_objects(
            Bucket=self.bucket_name,
            Key=keys
        )
        return res.get('Deleted', [])

    async def head_file(self, key: str, **kwargs) -> Union[StoredObject|None]:
        try:
            res = self.client.head_object(
                Bucket=self.bucket_name,
                Key=key,
            )
        except CosServiceError as e:  # type: CosServiceError
            e_info = e.get_digest_msg()
            if e_info['code'] == 'NoSuchResource':
                return None
            else:
                raise HeadFileFailed(eid=HeadFileFailed.Eid.head_file_failed)

        return StoredObject(
            storage_id=self.storage_config.storage_id,
            key=key,
        )