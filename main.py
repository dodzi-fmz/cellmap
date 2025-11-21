from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from jnius import autoclass, PythonJavaClass
import os
import sys
from cellmapview import CellMapView

LOCAL_DIR = os.path.dirname(__file__) if os.path.basename(sys.executable).startswith("python") else os.path.dirname(sys.executable)

def cell_info(self):
        context = autoclass('android.content.Context')
        tlph = autoclass('android.telephony.TelephonyManager')
        pyact = autoclass('org.kivy.android.PythonActivity')
        tlph_mgr = pyact.mActivity.getSystemService(context.TELEPHONY_SERVICE)
        cell_info = tlph_mgr.getAllCellInfo()

        tower = []

        for cell in cell_info:
             cid = cell.getCellIdentity().getCid()
             rssi = cell.getDbm()
             tower.append(f"GCI: {cid}, RSSI: {rssi}")
        self.root.ids.tower.text = "\n".join(tower)

class MainLayout(MDBoxLayout):
    pass


class CellMap(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file(os.path.join(LOCAL_DIR, 'main.kv'))

    def build(self):
        cell_info()
        return self.screen

if __name__ == "__main__":
    CellMap().run()
