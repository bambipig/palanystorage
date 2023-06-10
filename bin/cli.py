import sys
import pathlib


sys.path.append(
    pathlib.Path(__file__).parent.parent.joinpath('src').__str__()
)


from palanystorage.cli.main import app as cli_main_app


if __name__ == "__main__":
    cli_main_app()
