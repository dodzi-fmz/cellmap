from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from jnius import autoclass, PythonJavaClass
import os
import sys
from cellmapview import CellMapView

LOCAL_DIR = os.path.dirname(__file__) if os.path.basename(sys.executable).startswith("python") else os.path.dirname(sys.executable)

class MainLayout(MDBoxLayout):
    pass


class CellMap(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file(os.path.join(LOCAL_DIR, 'main.kv'))

    def build(self):
        self.cell_info()
        return self.screen

    def cell_info(self):
        context = autoclass('android.content.Context')
        tlph = autoclass('android.telephony.TelephonyManager')
        pyact = autoclass('org.kivy.android.PythonActivity')
        tlph_mgr = pyact.mActivity.getSystemService(context.TELEPHONY_SERVICE)
        cell_info = tlph_mgr.getAllCellInfo()

        tower = []

        for cell in cell_info:
            if isinstance(cell, autoclass('android.telephony.CellInfoGsm')):
                cell_id = cell.getCellIdentity()
                mcc = cell_id.getMcc()
                mnc = cell_id.getMnc()
                lac = cell_id.getLac()
                cid = cell_id.getCid()
                network = tlph.NETWORK_TYPE_GSM
                tower.append(f"GCI:{cid}, MCC:{mcc}, MNC:{mnc}, LAC:{lac}, Network_Type:{network}")
            elif isinstance(cell, autoclass('android.telephony.CellInfoCdma')):
                cell_id = cell.getCellIdentity()
                mcc = cell_id.getSystemId()
                mnc = cell_id.getNetworkId()
                lac = cell_id.getBasestationId()
                cid = cell_id.getBasestationId()
                network = tlph.NETWORK_TYPE_CDMA
                tower.append(f"GCI:{cid}, MCC:{mcc}, MNC:{mnc}, LAC:{lac}, Network_Type:{network}")
            elif isinstance(cell, autoclass('android.telephony.CellInfoLte')):
                cell_id = cell.getCellIdentity()
                mcc = cell_id.getMccString()
                mnc = cell_id.getMncString()
                lac = cell_id.getTac()
                cid = cell_id.getCi()
                network = tlph.NETWORK_TYPE_LTE
                tower.append(f"GCI:{cid}, MCC:{mcc}, MNC:{mnc}, LAC:{lac}, Network_Type:{network}")
            elif isinstance(cell, autoclass('android.telephony.CellInfoWcdma')):
                cell_id = cell.getCellIdentity()
                mcc = cell_id.getMcc()
                mnc = cell_id.getMnc()
                lac = cell_id.getLac()
                cid = cell_id.getCid()
                network = tlph.NETWORK_TYPE_UMTS
                tower.append(f"GCI:{cid}, MCC:{mcc}, MNC:{mnc}, LAC:{lac}, Network_Type:{network}")
            elif isinstance(cell, autoclass('android.telephony.CellInfoNr')):
                cell_id = cell.getCellIdentity()
                mcc = cell_id.getMccString()
                mnc = cell_id.getMncString()
                lac = cell_id.getTac()
                cid = cell_id.getNci()
                network = tlph.NETWORK_TYPE_NR
                tower.append(f"GCI:{cid}, MCC:{mcc}, MNC:{mnc}, LAC:{lac}, Network_Type:{network}")
            else:
                mcc = ""
                mnc = ""
                lac = ""
                cid = ""
                network = ""
                tower.append(f"GCI:{cid}, MCC:{mcc}, MNC:{mnc}, LAC:{lac}, Network_Type:{network}")
                continue
        self.root.ids.tower.text = "\n".join(tower)

if __name__ == "__main__":
    CellMap().run()