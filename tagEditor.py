import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from pycomm3 import LogixDriver
import time
import threading
import os


class MyGrid(Widget):
    plcip = ObjectProperty(None)
    plctag = ObjectProperty(None)
    ipstatus = ObjectProperty(None)
    tagread = ObjectProperty(None)
    tagwrite = ObjectProperty(None)
    statusread = ObjectProperty(None)
    plcpgmname = ObjectProperty(None)

    def checkipbtn(self):
        self.tagread.text = ""
        self.ipstatus.text = "checking for connection..."
        threading.Thread(target=self.checkplc).start()
   
    def checkplc(self):
        try:
            with LogixDriver(self.plcip.text) as plc:
                self.ipstatus.text = "Connection Success"
                self.plcpgmname.text = plc.get_plc_name()

        except:
            self.ipstatus.text = "Connection Failed"

    def retrievebtn(self):
        self.tagread.text = "attempting to load value..."
        threading.Thread(target=self.readtag).start()

    def readtag(self):
        try:
            with LogixDriver(self.plcip.text) as plc:
                tagrresult = str((plc.read(self.plctag.text)[1]))
                print(tagrresult)
                self.tagread.text = tagrresult
        except:
            self.tagread.text = "Read Failed..."

    def storebtn(self):
        self.statusread.text = "attempting to store tag..."
        threading.Thread(target=self.writetag).start()

    def writetag(self):
        try:
            with LogixDriver(self.plcip.text) as plc:
                plcintcon = int(self.tagwrite.text)
                print(plcintcon)
                plc.write(self.plctag.text, plcintcon)
                tagrresult1 = str((plc.read(self.plctag.text)[1]))
                self.tagread.text = tagrresult1
                self.statusread.text = "Write Successful"
        except:
            self.statusread.text = "Write Failed..."

    def fetchtags(self):
        try:
            os.remove("tags.csv")
        except:
            print("no csv")
        self.ipstatus.text = "Fetching Tags..."
        try:
            with LogixDriver(self.plcip.text) as plc:
                with open("tags.csv", "a") as f:
                    taglist = plc.get_tag_list()
                    for x in taglist:
                        print(str(x["tag_name"]) + "," + str(x["data_type_name"]) + "," + str(x["external_access"]), file=f) 
                    self.ipstatus.text = "Tags Saved"
        except:
            self.ipstatus.text = "Tag Download Failed"

    def clearbtn(self):
        self.ipstatus.text = ""
        self.plcip.text = ""
        self.plctag.text = ""
        self.tagread.text = ""
        self.tagwrite.text = ""

class MyApp(App): # <- Main Class
    def build(self):
        Window.size = (500,450)
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
