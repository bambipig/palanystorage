from palanystorage.schema import StorageConfigSchema, StoredObject, WriteProgressSchema
import oss2
from typing import Union, Callable


class PalAliossDialect:
    driver = 'pal_alioss'

    def __init__(self, storage_config: StorageConfigSchema):
        self.storage_config = storage_config
        self.auth = oss2.Auth(
            access_key_id=storage_config.access_key,
            access_key_secret=storage_config.access_key_secret)
        self.bucket = oss2.Bucket(
            auth=self.auth,
            endpoint=storage_config.inside_endpoint,
            bucket_name=storage_config.bucket,
        )  # type: oss2.Bucket

    async def ready(self, **kwargs):
        pass

    def write_progress_maker(self, wrote_bytes: int, total_bytes: int, **kwargs) -> WriteProgressSchema:
        extra = kwargs['extra']
        key = extra['key']
        return WriteProgressSchema(
            storage_id=self.storage_config.storage_id,
            key=key,
            wrote_bytes=wrote_bytes, total_bytes=total_bytes
        )

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

        res = oss2.resumable_upload(self.bucket, key=key, filename=file_path, progress_callback=progress_callback)  # type: oss2.models.PutObjectResult
        # return {'ret': {'hash': res.etag, 'key': key}, 'info': res}
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

        url = self.bucket.sign_url('GET', key=key, expires=expires)

        return StoredObject(
            storage_id=self.storage_config.storage_id,
            key=key,
            url=url,
        )

    async def delete_file(self, key: str, **kwargs) -> str:
        res = self.bucket.batch_delete_objects([key,])
        return res.deleted_keys[0]

    async def delete_files(self, keys: list[str], **kwargs) -> list[str]:
        res = self.bucket.batch_delete_objects(keys)
        return res.deleted_keys

    async def head_file(self, key: str, **kwargs) -> Union[StoredObject|None]:
        try:
            res = self.bucket.head_object(key)
        except oss2.exceptions.NotFound as _:
            return None

        return StoredObject(
            storage_id=self.storage_config.storage_id,
            key=key,
        )