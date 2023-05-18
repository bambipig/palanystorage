from .pal_alioss import PalAliossDialect


dialect_name = 'alioss'

drivers = [PalAliossDialect,]

plugin = {
    dialect_name: {
        _driver.driver: _driver
        for _driver in drivers
    }
}