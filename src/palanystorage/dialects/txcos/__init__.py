from .pal_txcos import PalTxcosDialect


dialect_name = 'txcos'

drivers = [PalTxcosDialect,]

plugin = {
    dialect_name: {
        _driver.driver: _driver
        for _driver in drivers
    }
}