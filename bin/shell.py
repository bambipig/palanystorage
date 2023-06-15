import sys
import pathlib
import os
import argparse

sys.path.append(
    pathlib.Path(__file__).parent.parent.joinpath('src').__str__()
)


parser = argparse.ArgumentParser()
parser.add_argument('--config')
args = parser.parse_args()
config_file_path = args.config

os.environ['CONFIG_FILE_PATH'] = config_file_path

# First create a config object from the traitlets library
from traitlets.config import Config
c = Config()

# Now we can set options as we would in a config file:
#   c.Class.config_value = value
# For example, we can set the exec_lines option of the InteractiveShellApp
# class to run some code when the IPython REPL starts
c.InteractiveShellApp.exec_lines = [
    # 'print("\\nimporting some things\\n")',
    # 'import math',
    # "math"
    'import os',
    'import anyconfig',
    'from palanystorage.engine import create_engine',
    'from palanystorage.schema import StorageConfigSchema',
    f'config_info = anyconfig.load("{config_file_path}")',
    f'storage_config = StorageConfigSchema(**config_info)',
]
c.InteractiveShell.colors = 'LightBG'
c.InteractiveShell.confirm_exit = False
c.TerminalIPythonApp.display_banner = False

# Now we start ipython with our configuration
import IPython
IPython.start_ipython(config=c)