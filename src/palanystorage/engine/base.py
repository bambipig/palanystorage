from palanystorage.schema import StoredObject, StorageConfigSchema


class Dialect:
    def __init__(self):
        pass

    async def ready(self, *args, **kwargs):
        pass

    async def write_file(self,  *args, **kwargs):
        pass

    async def read_file(self,  *args, **kwargs):
        pass

    async def meta_file(self,  *args, **kwargs):
        pass



class Engine:
    """
    Union Engine of Any Storage
    Every storage dialect need support all operate of this class.
    """

    dialect: Dialect

    def __init__(self, dialect: Dialect, config_schema: StorageConfigSchema):
        self.dialect = dialect
        self.config_schema = config_schema

    async def ready(self, *args, **kwargs):
        """
        TODO
        Ready state, can upload meta down
        :return:
        """
        return await self.dialect.ready(*args, **kwargs)

    async def write_file(self, file_path: str, key:str) -> StoredObject:
        """
        TODO
        Add File
        :param file_path:
        :param key:
        :return:
        """
        return await self.dialect.write_file(file_path, key)

    async def read_file(self, key: str):
        return await self.dialect.ready(key)


    async def meta_file(self, key: str) -> StoredObject:
        return await self.dialect.meta_file(key)
