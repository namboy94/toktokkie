from plugins.renamer.Renamer import Renamer

class PluginManager(object):

    def __init__(self, config):
        self.allPlugins = []
        self.allPlugins.append(Renamer())
        #New Plugins here

        self.activePlugins = []
        for plugin in self.allPlugins:
            if config[plugin.getName().lower()].lower() in ["true", "yes", "1"]:
                self.activePlugins.append(plugin)

    def getPlugins(self):
        return self.activePlugins