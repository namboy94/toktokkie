from plugins.renamer.RenamerPlugin import RenamerPlugin

"""
Class that manages plugins and checks which plugins to run
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class PluginManager(object):

    """
    Constructor
    Already checks which plugins to use
    @:param config - the config file's [plugin] section as a dictionary
    """
    def __init__(self, config):
        allPlugins = []
        allPlugins.append(RenamerPlugin())
        #New Plugins here

        self.activePlugins = []
        for plugin in allPlugins:
            if config[plugin.getName().lower()].lower() in ["true", "yes", "1"]:
                self.activePlugins.append(plugin)

    """
    Returns a list of plugins, which should be used by the user interface. (CLI or GUI)
    """
    def getPlugins(self):
        return self.activePlugins