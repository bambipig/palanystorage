from palanystorage.engine.base import Engine, Dialect
from palanystorage.loader import load_plugin
from palanystorage.schema import StorageConfigSchema


async def create_engine(dialect_name:str, driver:str, storage_config: StorageConfigSchema, **kwargs) -> Engine:
    dialect = load_plugin(dialect_name, driver)  # type: Dialect

    engine = Engine(dialect=dialect)

    return engine


