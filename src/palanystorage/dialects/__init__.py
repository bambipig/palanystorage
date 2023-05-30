from .alioss import plugin as alioss_plugin
from .qiniu import plugin as qiniu_plugin


plugins = {}
plugins.update(alioss_plugin)
plugins.update(qiniu_plugin)