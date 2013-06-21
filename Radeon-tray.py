#!/usr/bin/python3

# Copyright 2012 Francisco Pina Martins <f.pinamartins@gmail.com>
# This file is part of Radeon-tray.
# Radeon-tray is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Radeon-tray is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Radeon-tray.  If not, see <http://www.gnu.org/licenses/>.

import sys
from os import path
from PyQt4 import QtGui, QtCore

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent, method, profile, cards):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        
        self.setToolTip("Radeon-Tray")
        
        menu = QtGui.QMenu(parent)

        highAction = menu.addAction(QtGui.QIcon("high.svg"), "High Power")
        highAction.triggered.connect(lambda: power_method_set("profile", cards))
        highAction.triggered.connect(lambda: power_profile_set("high", cards))
        highAction.triggered.connect(lambda: self.setIcon(QtGui.QIcon("high.svg")))
        highAction.triggered.connect(lambda: lowAction.setEnabled(True))
        highAction.triggered.connect(lambda: midAction.setEnabled(True))
        highAction.triggered.connect(lambda: highAction.setEnabled(False))
        highAction.triggered.connect(lambda: autoAction.setEnabled(True))
        highAction.triggered.connect(lambda: dynpmAction.setEnabled(True))

        midAction = menu.addAction(QtGui.QIcon("mid.svg"), "Mid Power")
        midAction.triggered.connect(lambda: power_method_set("profile", cards))
        midAction.triggered.connect(lambda: power_profile_set("mid", cards))
        midAction.triggered.connect(lambda: self.setIcon(QtGui.QIcon("mid.svg")))
        midAction.triggered.connect(lambda: lowAction.setEnabled(True))
        midAction.triggered.connect(lambda: midAction.setEnabled(False))
        midAction.triggered.connect(lambda: highAction.setEnabled(True))
        midAction.triggered.connect(lambda: autoAction.setEnabled(True))
        midAction.triggered.connect(lambda: dynpmAction.setEnabled(True))

        lowAction = menu.addAction(QtGui.QIcon("low.svg"), "Low Power")
        lowAction.triggered.connect(lambda: power_method_set("profile", cards))
        lowAction.triggered.connect(lambda: power_profile_set("low", cards))
        lowAction.triggered.connect(lambda: self.setIcon(QtGui.QIcon("low.svg")))
        lowAction.triggered.connect(lambda: lowAction.setEnabled(False))
        lowAction.triggered.connect(lambda: midAction.setEnabled(True))
        lowAction.triggered.connect(lambda: highAction.setEnabled(True))
        lowAction.triggered.connect(lambda: autoAction.setEnabled(True))
        lowAction.triggered.connect(lambda: dynpmAction.setEnabled(True))

        autoAction = menu.addAction(QtGui.QIcon("auto.svg"), "Auto")
        autoAction.triggered.connect(lambda: power_method_set("profile", cards))
        autoAction.triggered.connect(lambda: power_profile_set("auto", cards))
        autoAction.triggered.connect(lambda: self.setIcon(QtGui.QIcon("auto.svg")))
        autoAction.triggered.connect(lambda: lowAction.setEnabled(True))
        autoAction.triggered.connect(lambda: midAction.setEnabled(True))
        autoAction.triggered.connect(lambda: highAction.setEnabled(True))
        autoAction.triggered.connect(lambda: autoAction.setEnabled(False))
        autoAction.triggered.connect(lambda: dynpmAction.setEnabled(True))
        
        dynpmAction = menu.addAction(QtGui.QIcon("dynpm.svg"), "Dynpm")
        dynpmAction.triggered.connect(lambda: power_profile_set("default", cards))
        dynpmAction.triggered.connect(lambda: power_method_set("dynpm", cards))
        dynpmAction.triggered.connect(lambda: self.setIcon(QtGui.QIcon("auto.svg")))
        dynpmAction.triggered.connect(lambda: lowAction.setEnabled(True))
        dynpmAction.triggered.connect(lambda: midAction.setEnabled(True))
        dynpmAction.triggered.connect(lambda: highAction.setEnabled(True))
        dynpmAction.triggered.connect(lambda: autoAction.setEnabled(True))
        dynpmAction.triggered.connect(lambda: dynpmAction.setEnabled(False))

        sep1 = menu.addSeparator()

        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(QtGui.qApp.quit)

        if profile == "low":
            lowAction.setEnabled(False)
        if profile == "mid":
            midAction.setEnabled(False)
        if profile == "high":
            highAction.setEnabled(False)
        if profile == "auto":
            autoAction.setEnabled(False)

        self.setContextMenu(menu)
        
        QtCore.QObject.connect(
            self,
            QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"),
            self.show_status)
    
    def show_status(self, act_reas):
        """Show current card status
        
        Reasons:
            0: unknown reason
            1: request for the context menu
            2: double clicked
            3: one click
            4: click with the middle button
        
        Icons:
            NoIcon, Information, Warning, Critical
        """
        if act_reas == 3:
            self.showMessage("Radeon-INFO",
                radeon_info_get(), self.Information, 10000)
    
    

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

def radeon_info_get():
    """Get the power info
    """
    cards = verifier()
    radeon_info = ""
    for xx in range(cards):
        radeon_info += "----- Card%d -----\n" % xx
        radeon_info += "Power method: %s\nPower profile: %s\n" % power_status_get(xx)
        with open("/sys/kernel/debug/dri/"+str(xx)+"/radeon_pm_info","r") as ff:
            radeon_info += ff.read().strip()
        radeon_info += "\n---------------"
    return radeon_info


def power_status_get(num=0):
    #Get the power status. Uses with to close the file immediatelly
    with open("/sys/class/drm/card"+str(num)+"/device/power_method","r") as f:
        power_method = f.readline().strip()
    with open("/sys/class/drm/card"+str(num)+"/device/power_profile","r") as f:
        power_profile = f.readline().strip()
    return power_method, power_profile

def power_profile_set(new_power_profile, cards):
    #Change the power profile
    for i in range(cards):
        with open("/sys/class/drm/card"+str(i)+"/device/power_profile","w") as f:
            print(new_power_profile)
            f.write(new_power_profile + "\n")

def power_method_set(new_power_method, cards):
    #Change the power method
    for i in range(cards):
        with open("/sys/class/drm/card"+str(i)+"/device/power_method","w") as f:
            f.write(new_power_method + "\n")


if __name__ == '__main__':
    main()