"""
Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    media-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    media-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with media-manager.  If not, see <http://www.gnu.org/licenses/>.
"""

from gfworks.templates.gtk3.Gtk3GridTemplate import Gtk3GridTemplate
from gfworks.templates.tk.TkGridTemplate import TkGridTemplate


class Globals(object):
    """
    A class storing various global imports and/or variables
    """

    # main gui selection
    MainGui = None
    try:
        from mainuserinterfaces.MainGUI import MainGUI as MainGui
    except ImportError:
        try:
            from mainuserinterfaces.MainTkGui import MainTkGui as MainGui
        except ImportError:
            try:
                from media_manager.mainuserinterfaces.MainGUI import MainGUI as MainGui
            except ImportError:
                from media_manager.mainuserinterfaces.MainTkGui import MainTkGui as MainGui
                
    # plugin gui selection
    RenamerGui = None
    try:
        from media_manager.plugins.renamer.userinterfaces.RenamerGUI import RenamerGUI as RenamerGui
    except ImportError:
        try:
            from media_manager.plugins.renamer.userinterfaces.RenamerTkGui import RenamerTkGui as RenamerGui
        except ImportError:
            try:
                from plugins.renamer.userinterfaces.RenamerGUI import RenamerGUI as RenamerGui
            except ImportError:
                from plugins.renamer.userinterfaces.RenamerTkGui import RenamerTkGui as RenamerGui
    IconizerGui = None
    try:
        from media_manager.plugins.iconizer.userinterfaces.IconizerGUI import IconizerGUI as IconizerGui
    except ImportError:
        try:
            from media_manager.plugins.iconizer.userinterfaces.IconizerTkGui import IconizerTkGui as IconizerGui
        except ImportError:
            try:
                from plugins.iconizer.userinterfaces.IconizerGUI import IconizerGUI as IconizerGui
            except ImportError:
                from plugins.iconizer.userinterfaces.IconizerTkGui import IconizerTkGui as IconizerGui
    BatchDownloadManagerGui = None
    try:
        from media_manager.plugins.batchdownloadmanager.userinterfaces.BatchDownloadManagerGUI \
            import BatchDownloadManagerGUI as BatchDownloadManagerGui
    except ImportError:
        try:
            from media_manager.plugins.batchdownloadmanager.userinterfaces.BatchDownloadManagerTkGui \
                import BatchDownloadManagerTkGui as BatchDownloadManagerGui
        except ImportError:
            try:
                from plugins.batchdownloadmanager.userinterfaces.BatchDownloadManagerGUI \
                    import BatchDownloadManagerGUI as BatchDownloadManagerGui
            except ImportError:
                from plugins.batchdownloadmanager.userinterfaces.BatchDownloadManagerTkGui \
                    import BatchDownloadManagerTkGui as BatchDownloadManagerGui

    selected_grid_gui_framework = Gtk3GridTemplate

    gtk3_gui_template = Gtk3GridTemplate
    tk_gui_template = TkGridTemplate
