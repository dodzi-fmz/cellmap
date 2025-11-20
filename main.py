from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.clock import Clock
from jnius import autoclass, PythonJavaClass, java_method, cast 
import os
import sys
from cellmapview import CellMapView

LOCAL_DIR = os.path.dirname(__file__) if os.path.basename(sys.executable).startswith("python") else os.path.dirname(sys.executable)

def cell_info(self):
        tlph = autoclass('android.telephony.TelephonyManager')
        pyact = autoclass('org.kivy.android.PythonActivity')
        tlph_mgr = pyact.mActivity.getSystemService('phone')
        cell_info = tlph_mgr.getAllCellInfo()

        tower = []

        for cell in cell_info:
             cid = cell.getCellId
             rssi = cell.getDbm()
             tower.append(f"GCI: {cid}, RSSI: {rssi}")
        self.root.ids.tower.text = "\n".join(tower)

class MainLayout(MDBoxLayout):
    pass


class CellMap(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file(LOCAL_DIR, 'main.kv')

    def build(self):
        Clock.schedule_interval(self.cell_info, 5)
        return self.screen

if __name__ == "__main__":
    CellMap().run()
