from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy_garden.mapview import MapMarker
from jnius import autoclass
import requests
import json
import os
import sys

LOCAL_DIR = os.path.dirname(__file__) if os.path.basename(sys.executable).startswith("python") else os.path.dirname(sys.executable)

API_KEY = "pk.fa0f14722d93d02d74bc66063891aa10"

url = "https://opencellid.org/cell/get"

class MainLayout(MDBoxLayout):
    pass

class CellMap(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

    def build(self):
        self.screen = Builder.load_file(os.path.join(LOCAL_DIR, 'main.kv'))
        return self.screen
    
    def on_start(self):
        Clock.schedule_interval(self.cell_info, 5)

    def clear_map(self):
        mapview = self.root.ids.map
        for child in list(mapview.children):
            if isinstance(child, MapMarker):
                mapview.remove_widget(child)

    def cell_info(self, dt):
        context = autoclass('android.content.Context')
        tlph = autoclass('android.telephony.TelephonyManager')
        pyact = autoclass('org.kivy.android.PythonActivity')
        tlph_mgr = pyact.mActivity.getSystemService(context.TELEPHONY_SERVICE)
        cell_info = tlph_mgr.getAllCellInfo()

        cells = []
        markers = []
        self.clear_map()
        mapview = self.root.ids.map

        for cell in cell_info:
            if isinstance(cell, autoclass('android.telephony.CellInfoGsm')):
                cell_id = cell.getCellIdentity()
                lac = cell_id.getLac()
                cid = cell_id.getCid()
                rssi = cell.getCellSignalStrength().getRssi()
                network = tlph.NETWORK_TYPE_GSM
                cells.append({"lac":lac, "cid": cid, "psc": 0})
                markers.append(f"GCI:{cid}, RSSI:{rssi}, LAC:{lac}, Network_Type:{network}")
            elif isinstance(cell, autoclass('android.telephony.CellInfoCdma')):
                cell_id = cell.getCellIdentity()
                cid = cell_id.getBasestationId()
                lac = cell_id.getBasestationId()
                rssi = cell.getCellSignalStrength().getRssi()
                network = tlph.NETWORK_TYPE_CDMA
                cells.append({"lac":lac, "cid": cid, "psc": 0})
                markers.append(f"GCI:{cid}, RSSI:{rssi}, LAC:{lac}, Network_Type:{network}")
            elif isinstance(cell, autoclass('android.telephony.CellInfoLte')):
                cell_id = cell.getCellIdentity()
                mcc = cell_id.getMccString()
                mnc = cell_id.getMncString()
                lac = cell_id.getTac()
                cid = cell_id.getCi()
                rssi = cell.getCellSignalStrength().getRssi()
                network = tlph.NETWORK_TYPE_LTE
                cells.append({"lac":lac, "cid": cid, "psc": 0})
                markers.append(f"GCI:{cid}, RSSI:{rssi}, MCC:{mcc}, MNC:{mnc}, LAC:{lac}, Network_Type:{network}")
            elif isinstance(cell, autoclass('android.telephony.CellInfoWcdma')):
                cell_id = cell.getCellIdentity()
                cid = cell_id.getCid()
                lac = cell_id.getLac()
                rssi = cell.getCellSignalStrength().getRssi()
                network = tlph.NETWORK_TYPE_UMTS
                cells.append({"lac":lac, "cid": cid, "psc": 0})
                markers.append(f"GCI:{cid}, RSSI:{rssi}, LAC:{lac}, Network_Type:{network}")
            elif isinstance(cell, autoclass('android.telephony.CellInfoNr')):
                cell_id = cell.getCellIdentity()
                cid = cell_id.getNci()
                lac = cell_id.getTac()
                rssi = cell.getCellSignalStrength().getRssi()
                network = tlph.NETWORK_TYPE_NR
                cells.append({"lac":lac, "cid": cid, "psc": 0})
                markers.append(f"GCI:{cid}, RSSI:{rssi}, LAC:{lac}, Network_Type:{network}")
            else:
                mcc = ""
                mnc = ""
                lac = ""
                cid = ""
                rssi = ""
                network = ""
                continue
        
        params = {
            "token": API_KEY,
            "radio": "lte",
            "mcc": mcc,
            "mnc": mnc,
            "cells": cells,
            "address": 0 
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data and data.get('status') == 'ok':
            lat = data.get("lat")
            lon = data.get("lon")

            marker = MapMarker(lat=lat, lon=lon)
            mapview.add_widget(marker)
        else:
            lat = ""
            lon = ""

        self.root.ids.info.text = "\n".join(markers)

if __name__ == "__main__":
    CellMap().run()
