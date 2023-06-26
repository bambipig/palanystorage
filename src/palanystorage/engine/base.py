from palanystorage.schema import StoredObject, StorageConfigSchema, WriteProgressSchema
from typing import Union, Callable
from os import PathLike
from palanystorage.log import logger


class Dialect:
    def __init__(self, storage_config: StorageConfigSchema):
        pass

    async def ready(self, *args, **kwargs):
        pass

    def write_progress_maker(self, *args, **kwargs) -> WriteProgressSchema:
        pass

    async def write_file(self, *args, **kwargs) -> StoredObject:
        pass

    async def read_file(self, *args, **kwargs) -> StoredObject:
        pass

    async def meta_file(self, *args, **kwargs) -> StoredObject:
        pass

    async def delete_file(self, *args, **kwargs) -> None:
        pass

    async def delete_files(self, *args, **kwargs) -> list[str]:
        pass

    async def head_file(self, *args, **kwargs):
        pass

class Engine:
    """
    Union Engine of Any Storage
    Every storage dialect need support all operate of this class.
    """

    dialect: Dialect

    def __init__(self, dialect: Dialect, storage_config: StorageConfigSchema):
        self.dialect = dialect
        self._storage_config = storage_config

    @property
    def root_path(self) -> Union[str|PathLike]:
        return self._storage_config.root_path

    async def ready(self, **kwargs):
        """
        TODO
        Ready state, can upload meta down
        :return:
        """
        return await self.dialect.ready(**kwargs)

    def write_progress_maker(self, *args, **kwargs) -> WriteProgressSchema:
        return self.dialect.write_progress_maker(*args, **kwargs)

    def progress_callback_wrapper(self, outside_progress_callback: Callable, extra: dict):
        def _progress_callback(*args, **kwargs):
            kwargs['extra'] = extra
            write_progress_schema = self.write_progress_maker(*args, **kwargs)
            outside_progress_callback(write_progress_schema)
        return _progress_callback

    async def write_file(
        self,
        file_path: str,
        key: str,
        outside_progress_callback: Union[Callable] = None,
        **kwargs) -> StoredObject:
        """
        TODO
        Add File
        :param file_path:
        :param key:
        :param outside_progress_callback:
        :return:
        """
        if outside_progress_callback is None:
            outside_progress_callback = lambda *a, **kw: None

        logger.info(f'Storage Writer Received ProgressCallback: <{outside_progress_callback}>')
        kwargs['file_path'] = file_path
        kwargs['key'] = key
        kwargs['progress_callback'] = self.progress_callback_wrapper(outside_progress_callback, extra=kwargs)
        return await self.dialect.write_file(**kwargs)

    async def read_file(self, key: str, **kwargs):
        """
        TODO
        :param key:
        :param args:
        :param kwargs:
        :return:
        """
        kwargs['key'] = key
        return await self.dialect.read_file(**kwargs)

    async def meta_file(self, key: str, expires: int, **kwargs) -> StoredObject:
        """
        TODO
        :param key:
        :param args:
        :param kwargs:
        :return:
        """

        kwargs['key'] = key
        kwargs['expires'] = expires
        return await self.dialect.meta_file(**kwargs)

    async def delete_file(self, key: str, **kwargs):
        kwargs['key'] = key
        return await self.dialect.delete_file(**kwargs)

    async def delete_files(self, keys: list[str], **kwargs):
        kwargs['keys'] = keys
        return await self.dialect.delete_files(**kwargs)

    async def head_file(self, key: str, **kwargs):
        kwargs['key'] = key
        return await self.dialect.head_file(**kwargs)