from plugins.renamer.RenamerPlugin import RenamerPlugin
from plugins.xdccSearchAndDownload.XDCCPlugin import XDCCPlugin
from plugins.iconizer.IconizerPlugin import IconizerPlugin

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
        allPlugins.append(XDCCPlugin())
        allPlugins.append(IconizerPlugin())
        #New Plugins here

        #overrides reading from config
        self.activePlugins = allPlugins
        """
        self.activePlugins = []
        for plugin in allPlugins:
            if config[plugin.getConfigTag()].lower() in ["true", "yes", "1"]:
                self.activePlugins.append(plugin)
        """

    """
    Returns a list of plugins, which should be used by the user interface. (CLI or GUI)
    """
    def getPlugins(self):
        return self.activePlugins