"""
Generic Plugin that serves as a unified interface for the plugins.
@author Hermann Krumrey <hermann@krumreyh.com>
"""
class GenericPlugin(object):

    def getName(self):
        raise NotImplementedError()

    def startCLI(self, parentCLI):
        raise NotImplementedError()

    def startGUI(self, parentGUI):
        raise NotImplementedError()