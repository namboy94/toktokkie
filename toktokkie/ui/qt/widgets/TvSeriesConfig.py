import os
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from toktokkie.utils.metadata.media_types.TvSeries import TvSeries
from toktokkie.ui.qt.pyuic.tv_series_config import Ui_TvSeriesConfig


class TvSeriesConfig(QWidget, Ui_TvSeriesConfig):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.tv_series = None

    def set_data(self, tv_series: TvSeries, child: str = "main"):
        self.series_name_edit.setText(tv_series.name)
        self.folder_icon_label.setPixmap(QPixmap(os.path.join(tv_series.path, ".meta/icons/main.png")))

    def store_data(self):
        pass

    def load_tvdb_data(self):
        pass
