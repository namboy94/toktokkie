from plugins.genericPlugin.GenericPlugin import GenericPlugin
from plugins.batchDownloadManager.userinterfaces.BatchDownloadManagerCLI import BatchDownloadManagerCLI
from plugins.batchDownloadManager.userinterfaces.BatchDownloadManagerGUI import BatchDownloadManagerGUI

"""
Class that handles the calls to the BatchDownloadManager
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class BatchDownloadManagerPlugin(GenericPlugin):

    """
    @:return "Batch Download Manager"
    """
    def getName(self):
        return "Batch Download Manager"

    """
    @:return "batch-download"
    """
    def getConfigTag(self):
        return "batch-download"

    """
    @:return "batch download"
    """
    def getCommandName(self):
        return "batch download"

    """
    Starts the CLI
    """
    def startCLI(self, parentCLI):
        BatchDownloadManagerCLI().start()

    """
    Starts the GUI, while hiding the parent until finished
    """
    def startGUI(self, parentGUI):
        BatchDownloadManagerGUI(parentGUI, "Batch Download Manager").start()
