from palanystorage.schema import StorageConfigSchema, StoredObject
from typing import Union
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
        pass

    async def write_file(self, file_path: str, key: str, **kwargs):
        """
        Write File
        :param file_path:
        :param key:
        :param kwargs:
        :return:
        """
        token = self.get_upload_token(key, 300)
        try:
            put_file(token, key, file_path)
        except Exception as e:
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

    async def delete_file(self, key: str, **kwargs) -> str:
        await self.delete_files([key])
        return key

    async def delete_files(self, keys: list[str], **kwargs) -> list[str]:
        ops = build_batch_delete(self.bucket_name, keys)
        try:
            ret, info = self.bucket_mgr.batch(ops)
        except Exception as e:
            raise DeleteFileFailed(eid=DeleteFileFailed.Eid.storage_delete_failed)
        return keys

    async def head_file(self, key: str, **kwargs) -> Union[StoredObject|None]:
        ret, _ = self.bucket_mgr.stat(self.bucket_name, key)

        if ret is None:
            return None

        return StoredObject(
            storage_id=self.storage_config.storage_id,
            key=key,
        )