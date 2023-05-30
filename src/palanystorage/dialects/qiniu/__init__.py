from .pal_qiniu import PalQiniuDialect


dialect_name = 'qiniu'

drivers = [PalQiniuDialect,]

plugin = {
    dialect_name: {
        _driver.driver: _driver
        for _driver in drivers
    }
}