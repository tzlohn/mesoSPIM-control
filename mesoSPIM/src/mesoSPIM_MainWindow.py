'''
mesoSPIM MainWindow

'''

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi

from .mesoSPIM_CameraWindow import mesoSPIM_CameraWindow
from .mesoSPIM_AcquisitionManagerWindow import mesoSPIM_AcquisitionManagerWindow


class mesoSPIM_MainWindow(QtWidgets.QMainWindow):
    '''
    Main application window which instantiates worker objects and moves them
    to a thread.
    '''
    def __init__(self, config=None):
        super().__init__()
        loadUi('gui/mesoSPIM_MainWindow.ui', self)
        self.setWindowTitle('Thread Template')

        self.camera_window = mesoSPIM_CameraWindow()
        self.camera_window.show()

        self.acquisiton_manager_window = mesoSPIM_AcquisitionManagerWindow(self)
        self.acquisiton_manager_window.show()