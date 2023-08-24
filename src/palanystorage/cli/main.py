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


@app.command('shell')
def shell(
    as_config_file: str,
):
    from traitlets.config import Config
    c = Config()
    c.InteractiveShellApp.exec_lines = [
        # 'print("\\nimporting some things\\n")',
        # 'import math',
        # "math"
        'import os',
        'import anyconfig',
        'from palanystorage.engine import create_engine',
        'from palanystorage.schema import StorageConfigSchema',
        f'config_info = anyconfig.load("{as_config_file}")',
        f'storage_config = StorageConfigSchema(**config_info)',
    ]
    c.InteractiveShell.colors = 'LightBG'
    c.InteractiveShell.confirm_exit = False
    c.TerminalIPythonApp.display_banner = False

    # Now we start ipython with our configuration
    import IPython
    IPython.start_ipython(config=c)



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
            await engine.write_file(f_path.__str__(), key)



@app.command('upload')
def upload(
    src_dir: str,
    key_prefix: str,
    config_file: str = Option(),
):
    loop.run_until_complete(
        _upload(src_dir, key_prefix, config_file)
    )