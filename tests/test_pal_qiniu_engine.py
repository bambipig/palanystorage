import pytest
import uuid
from palanystorage.schema import StorageConfigSchema
from palanystorage.engine import Engine
from palanystorage.dialects.qiniu import pal_qiniu


class TestPalQiniu:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_key = f'{uuid.uuid4().hex}.txt'
        self.test_expires = 3600

    @pytest.mark.asyncio
    async def test_ready(self, config: StorageConfigSchema, engine: Engine):
        assert config.driver == pal_qiniu.PalQiniuDialect.driver
        await engine.ready()

    def test_ready_sync(self, config: StorageConfigSchema, engine: Engine):
        assert config.driver == pal_qiniu.PalQiniuDialect.driver
        engine.ready_sync()

    @pytest.mark.asyncio
    async def test_retrieve_upload_token(self, config: StorageConfigSchema, engine: Engine):
        token = await engine.retrieve_upload_token(key=self.test_key, expires=self.test_expires)
        assert isinstance(token, dict)

    def test_retrieve_upload_token_sync(self, config: StorageConfigSchema, engine: Engine):
        token = engine.retrieve_upload_token_sync(key=self.test_key, expires=self.test_expires)
        assert isinstance(token, dict)
