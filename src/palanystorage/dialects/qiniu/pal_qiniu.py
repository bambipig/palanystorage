import traceback

from palanystorage.schema import StorageConfigSchema, StoredObject, WriteProgressSchema
from typing import Union, Callable, Optional, AnyStr, List
from qiniu import Auth, BucketManager, put_file, build_batch_delete
from palanystorage.exceptions import WriteFileFailed, DeleteFileFailed


class PalQiniuDialect:
    driver = 'pal_qiniu'

    def __init__(self, storage_config: StorageConfigSchema):
        self.storage_config = storage_config
        self.bucket_name = storage_config.bucket
        self.q = Auth(storage_config.access_key, storage_config.access_key_secret)
        self.bucket_mgr = BucketManager(self.q)  # type: BucketManager

    def get_upload_token(self, key, expires, policy=None):
        token = self.q.upload_token(self.bucket_name, key, expires, policy)
        return token

    async def ready(self, **kwargs):
        return self.ready_sync(**kwargs)

    def ready_sync(self, **kwargs):
        pass

    def write_progress_maker(self, wrote_bytes: int, total_bytes: int, **kwargs) -> WriteProgressSchema:
        extra = kwargs['extra']
        key = extra['key']
        return WriteProgressSchema(
            storage_id=self.storage_config.storage_id,
            key=key,
            wrote_bytes=wrote_bytes, total_bytes=total_bytes
        )

    async def write_file(self, file_path: AnyStr, key: AnyStr, progress: Callable, **kwargs) -> StoredObject:
        return self.write_file_sync(file_path, key, progress, **kwargs)

    def write_file_sync(self, file_path: str, key: str, progress_callback: Callable, **kwargs):
        """
        Write File
        :param file_path:
        :param key:
        :param progress_callback:
        :param kwargs:
        :return:
        """
        token = self.get_upload_token(key, 300)
        # print('progress_callback', progress_callback)
        try:
            put_file(token, key, file_path, progress_handler=progress_callback)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            raise WriteFileFailed(eid=WriteFileFailed.Eid.storage_upload_failed)

        return StoredObject(
            storage_id=self.storage_config.storage_id,
            key=key,
        )

    async def read_file(self, key: AnyStr, **kwargs):
        return self.read_file_sync(key, **kwargs)

    def read_file_sync(self, key: str, **kwargs):
        """
        Read File
        :param key:
        :param kwargs:
        :return:
        """
        pass

    async def meta_file(self, key: AnyStr, expires: int, **kwargs) -> StoredObject:
        return self.meta_file_sync(key, expires, **kwargs)

    def meta_file_sync(self, key: str, expires: int, **kwargs) -> StoredObject:
        """
        Meta file
        :param key:
        :param kwargs:
        :return:
        """

        oe = self.storage_config.outside_endpoint
        if not oe.endswith('/'):
            oe = oe + '/'

        base_url = oe + key
        url = self.q.private_download_url(base_url, expires=expires)

        return StoredObject(
            storage_id=self.storage_config.storage_id,
            key=key,
            url=url,
        )

    async def delete_file(self, key: AnyStr, **kwargs) -> AnyStr:
        return self.delete_file_sync(key, **kwargs)

    def delete_file_sync(self, key: str, **kwargs) -> str:
        self.delete_files_sync([key])
        return key

    async def delete_files(self, keys: List[AnyStr], **kwargs) -> List[AnyStr]:
        return self.delete_files_sync(keys, **kwargs)

    def delete_files_sync(self, keys: List[AnyStr], **kwargs) -> List[AnyStr]:
        ops = build_batch_delete(self.bucket_name, keys)
        try:
            ret, info = self.bucket_mgr.batch(ops)
        except Exception as e:
            raise DeleteFileFailed(eid=DeleteFileFailed.Eid.storage_delete_failed)
        return keys

    async def head_file(self, key: AnyStr, **kwargs) -> StoredObject:
        return self.head_file_sync(key, **kwargs)

    def head_file_sync(self, key: str, **kwargs) -> Optional[StoredObject]:
        ret, _ = self.bucket_mgr.stat(self.bucket_name, key)

        if ret is None:
            return None

        return StoredObject(
            storage_id=self.storage_config.storage_id,
            key=key,
        )
