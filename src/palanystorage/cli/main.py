import typer
from typer import Option
import pathlib
import os
import anyconfig
from palanystorage.engine import create_engine
from palanystorage.schema import StorageConfigSchema
import asyncio
app = typer.Typer(name='palas')


loop = asyncio.get_event_loop()


async def _upload(
    src_dir: str,
    key_prefix: str,
    config_file: str = Option(),
):
    config_info = anyconfig.load(config_file)
    storage_config = StorageConfigSchema(**config_info)

    if not key_prefix.endswith('/'):
        key_prefix = key_prefix + '/'

    engine = await create_engine(
        dialect_name=storage_config.dialect,
        driver=storage_config.driver,
        storage_config=storage_config
    )

    root_abs_path = pathlib.Path(src_dir).expanduser().absolute()
    for root, _, files in os.walk(pathlib.Path(root_abs_path)):
        for f in files:
            f_path = pathlib.Path(root).joinpath(f)
            key = f_path.relative_to(root_abs_path).__str__()
            key = f'{key_prefix}{key}'
            print(f_path)
            print(key)
            await engine.write_file(f_path, key)



@app.command('upload')
def upload(
    src_dir: str,
    key_prefix: str,
    config_file: str = Option(),
):
    loop.run_until_complete(
        _upload(src_dir, key_prefix, config_file)
    )