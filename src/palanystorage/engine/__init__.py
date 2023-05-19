from palanystorage.engine.base import Engine, Dialect
from palanystorage.loader import load_plugin
from palanystorage.schema import StorageConfigSchema


async def create_engine(dialect_name:str, driver:str, storage_config: StorageConfigSchema, **kwargs) -> Engine:
    dialect_class = load_plugin(dialect_name, driver)  # type: type[Dialect]

    dialect = dialect_class(storage_config=storage_config)  # type: Dialect
    engine = Engine(dialect=dialect, storage_config=storage_config)

    return engine


