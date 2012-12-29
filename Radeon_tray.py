#!/usr/bin/python3

#See:
#http://stackoverflow.com/questions/893984/pyqt-show-menu-in-a-system-tray-application


import sys
from os import path
from PyQt4 import QtGui

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent, method, profile, cards):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)

        current_methodAction = menu.addAction(QtGui.QIcon("low.svg"), "Current power method: " + method)

        sep0 = menu.addSeparator()

        highAction = menu.addAction(QtGui.QIcon("high.svg"), "High Power")
        highAction.triggered.connect(lambda: power_profile_set("high", cards))
        highAction.triggered.connect(lambda: self.setIcon(QtGui.QIcon("high.svg")))
        highAction.triggered.connect(lambda: lowAction.setEnabled(True))
        highAction.triggered.connect(lambda: midAction.setEnabled(True))
        highAction.triggered.connect(lambda: highAction.setEnabled(False))
        highAction.triggered.connect(lambda: autoAction.setEnabled(True))

        midAction = menu.addAction(QtGui.QIcon("mid.svg"), "Mid Power")
        midAction.triggered.connect(lambda: power_profile_set("mid", cards))
        midAction.triggered.connect(lambda: self.setIcon(QtGui.QIcon("mid.svg")))
        midAction.triggered.connect(lambda: lowAction.setEnabled(True))
        midAction.triggered.connect(lambda: midAction.setEnabled(False))
        midAction.triggered.connect(lambda: highAction.setEnabled(True))
        midAction.triggered.connect(lambda: autoAction.setEnabled(True))

        lowAction = menu.addAction(QtGui.QIcon("low.svg"), "Low Power")
        lowAction.triggered.connect(lambda: power_profile_set("low", cards))
        lowAction.triggered.connect(lambda: self.setIcon(QtGui.QIcon("low.svg")))
        lowAction.triggered.connect(lambda: lowAction.setEnabled(False))
        lowAction.triggered.connect(lambda: midAction.setEnabled(True))
        lowAction.triggered.connect(lambda: highAction.setEnabled(True))
        lowAction.triggered.connect(lambda: autoAction.setEnabled(True))

        autoAction = menu.addAction(QtGui.QIcon("auto.svg"), "Auto")
        autoAction.triggered.connect(lambda: power_profile_set("auto", cards))
        autoAction.triggered.connect(lambda: self.setIcon(QtGui.QIcon("auto.svg")))
        autoAction.triggered.connect(lambda: lowAction.setEnabled(True))
        autoAction.triggered.connect(lambda: midAction.setEnabled(True))
        autoAction.triggered.connect(lambda: highAction.setEnabled(True))
        autoAction.triggered.connect(lambda: autoAction.setEnabled(False))

        sep1 = menu.addSeparator()

        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(QtGui.qApp.quit)

        self.setContextMenu(menu)


def main():
    #Main function
    cards = verifier()
    init_method, init_profile = power_status_get()

    if init_method == "dynpm":
        icon = "dynpm.svg"
    else:
        icon = init_profile + ".svg"

    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(icon), w, init_method, init_profile, cards)

    trayIcon.show()
    sys.exit(app.exec_())

def verifier():
    #First we verify how many cards we are dealing with, if any. Quit if none
    #are found.
    cards = 0
    if path.isdir("/sys/class/drm/card0"):
        cards += 1
    if path.isdir("/sys/class/drm/card1"):
        cards += 1
    if cards == 0:
        sys.exit("No suitable cards found.\nAre you using the OSS Radeon \
drivers?\nExiting the program.")
    return cards

def power_status_get():
    with open("/sys/class/drm/card0/device/power_method","r") as f:
        power_method = f.readline().strip()
    with open("/sys/class/drm/card0/device/power_profile","r") as f:
        power_profile = f.readline().strip()
    return power_method, power_profile

def power_profile_set(new_power_profile, cards):
    #Change the power profile
    for i in range(cards):
        with open("/sys/class/drm/card%s/device/power_profile" %(i),"w") as f:
            f.write(new_power_profile + "\n")

def power_method_set(new_power_method, cards):
    #Change the power method
    for i in range(cards):
        with open("/sys/class/drm/card%s/device/power_method" %(i),"w") as f:
            f.write(new_power_method + "\n")


if __name__ == '__main__':
    main()