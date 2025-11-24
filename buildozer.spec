[app]

title = CellMap
package.name = cellmap
package.domain = org.inside

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ttf

version = 0.0.2

requirements = python3,kivy==2.3.0,kivymd==1.2.0,pyjnius,android,sdl2,mapview,openssl,requests,numpy,pillow,charset_normalizer,chardet,idna,urllib3,certifi,opencellid

orientation = portrait

android.permissions = android.permission.INTERNET,android.permission.ACCESS_NETWORK_STATE,android.permission.ACCESS_COARSE_LOCATION,android.permission.ACCESS_FINE_LOCATION,android.permission.READ_PHONE_STATE
android.enable_androidx = True
android.debug_artifact = apk

fullscreen = 0

android.logcat_filters = *:S python:D