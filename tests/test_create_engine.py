import pytest

from palanystorage.engine import create_engine_sync, Engine, create_engine
from palanystorage.schema import StorageConfigSchema


@pytest.mark.asyncio
async def test_create_engine(config: StorageConfigSchema):
    engine = await create_engine(dialect_name=config.dialect, driver=config.driver, storage_config=config)
    assert isinstance(engine, Engine)


def test_create_engine_sync(config: StorageConfigSchema):
    engine = create_engine_sync(
        dialect_name=config.dialect,
        driver=config.driver,
        storage_config=config)
    assert isinstance(engine, Engine)
