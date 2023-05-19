from palanystorage.schema import StoredObject, StorageConfigSchema


class Dialect:
    def __init__(self, storage_config: StorageConfigSchema):
        pass

    async def ready(self, **kwargs):
        pass

    async def write_file(self, **kwargs) -> StoredObject:
        pass

    async def read_file(self, **kwargs) -> StoredObject:
        pass

    async def meta_file(self, **kwargs) -> StoredObject:
        pass



class Engine:
    """
    Union Engine of Any Storage
    Every storage dialect need support all operate of this class.
    """

    dialect: Dialect

    def __init__(self, dialect: Dialect):
        self.dialect = dialect

    async def ready(self, **kwargs):
        """
        TODO
        Ready state, can upload meta down
        :return:
        """
        return await self.dialect.ready(**kwargs)

    async def write_file(self, file_path: str, key: str, **kwargs) -> StoredObject:
        """
        TODO
        Add File
        :param file_path:
        :param key:
        :return:
        """
        kwargs['file_path'] = file_path
        kwargs['key'] = key
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

    async def meta_file(self, key: str, *args, **kwargs) -> StoredObject:
        """
        TODO
        :param key:
        :param args:
        :param kwargs:
        :return:
        """

        kwargs['key'] = key
        return await self.dialect.meta_file(**kwargs)
