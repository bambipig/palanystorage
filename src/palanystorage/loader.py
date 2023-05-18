from palanystorage.dialects import plugins
from .exceptions import UnknownDriver, UnknownDialect


def load_plugin(dialect_name:str, driver:str):
    dialect_drivers = plugins.get(dialect_name, None)
    if dialect_drivers is None:
        raise UnknownDialect('Unknown dialect [{}].'.format(dialect_name))

    dialect = dialect_drivers.get(driver, None)
    if dialect is None:
        raise UnknownDriver('Unknown driver [{}].'.format(driver))

    return dialect
