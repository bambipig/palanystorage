from .alioss import plugin as alioss_plugin
from .qiniu import plugin as qiniu_plugin
from .txcos import plugin as txcos_plugin


plugins = {}
plugins.update(alioss_plugin)
plugins.update(qiniu_plugin)
plugins.update(txcos_plugin)