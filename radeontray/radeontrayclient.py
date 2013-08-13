#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Client module

Copyright 2012-2013 Francisco Pina Martins <f.pinamartins@gmail.com>
and Mirco Tracolli.
This file is part of Radeon-tray.
Radeon-tray is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Radeon-tray is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Radeon-tray.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import zmq
from os import path
from PyQt4 import QtGui, QtCore
from .utils import last_power_status_get, \
    power_method_set, \
    power_profile_set, \
    power_status_get, \
    radeon_info_get, \
    verifier, \
    paths_verification,\
    icon_path

MAJVER = sys.version_info.major
HOME = path.expanduser("~") + "/"
PORT = "5556"
CONTEXT = None
SOCKET = None

ICONPATH = icon_path()

HIGHPATH = ICONPATH + "/radeon-tray-high.svg"
MIDPATH = ICONPATH + "/radeon-tray-mid.svg"
LOWPATH = ICONPATH + "/radeon-tray-low.svg"
AUTOPATH = ICONPATH + "/radeon-tray-auto.svg"
DYNPMPATH = ICONPATH + "/radeon-tray-dynpm.svg"
DEFAULTPATH = ICONPATH + "/radeon-tray-default.svg"
NOPERM = """"You don't have the permission to write card's
settings, check the official site for information!"""

class SystemTrayIcon(QtGui.QSystemTrayIcon):
    """Tray icon program for Radeon driver with kms
    """

    def __init__(self, icon, parent, method, profile, cards):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)

        self.setToolTip("Radeon-Tray")
        self.method = method
        self.profile = profile
        self.cards = cards

        menu = QtGui.QMenu(parent)

        self.high_action = menu.addAction(QtGui.QIcon(HIGHPATH), "High Power")
        self.high_action.triggered.connect(self.activate_high)

        self.mid_action = menu.addAction(QtGui.QIcon(MIDPATH), "Mid Power")
        self.mid_action.triggered.connect(self.activate_mid)

        self.low_action = menu.addAction(QtGui.QIcon(LOWPATH), "Low Power")
        self.low_action.triggered.connect(self.activate_low)

        self.auto_action = menu.addAction(QtGui.QIcon(AUTOPATH), "Auto")
        self.auto_action.triggered.connect(self.activate_auto)

        self.dynpm_action = menu.addAction(QtGui.QIcon(DYNPMPATH), "Dynpm")
        self.dynpm_action.triggered.connect(self.activate_dynpm)

        menu.addSeparator()

        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(QtGui.qApp.quit)

        self.setContextMenu(menu)

        # Connect object to activated signal to grab single click
        # on tray icon
        QtCore.QObject.connect(
            self,
            QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"),
            self.show_status)
        
        self.check_status()

    def activate_high(self):
        """Activate high profile
        """
        if not power_method_set("profile", self.cards, home=HOME, client=SOCKET) or\
            not power_profile_set("high", self.cards, home=HOME, client=SOCKET):
            self.showMessage("Error",
                NOPERM, self.Critical, 10000)
            return
        self.setIcon(QtGui.QIcon(HIGHPATH))
        self.low_action.setEnabled(True)
        self.mid_action.setEnabled(True)
        self.high_action.setEnabled(False)
        self.auto_action.setEnabled(True)
        self.dynpm_action.setEnabled(True)

    def activate_mid(self):
        """Activate mid profile
        """
        if not power_method_set("profile", self.cards, home=HOME, client=SOCKET) or\
            not power_profile_set("mid", self.cards, home=HOME, client=SOCKET):
            self.showMessage("Error",
                NOPERM, self.Critical, 10000)
            return
        self.setIcon(QtGui.QIcon(MIDPATH))
        self.low_action.setEnabled(True)
        self.mid_action.setEnabled(False)
        self.high_action.setEnabled(True)
        self.auto_action.setEnabled(True)
        self.dynpm_action.setEnabled(True)

    def activate_low(self):
        """Activate low profile
        """
        if not power_method_set("profile", self.cards, home=HOME, client=SOCKET) or\
            not power_profile_set("low", self.cards, home=HOME, client=SOCKET):
            self.showMessage("Error",
                NOPERM, self.Critical, 10000)
            return
        self.setIcon(QtGui.QIcon(LOWPATH))
        self.low_action.setEnabled(False)
        self.mid_action.setEnabled(True)
        self.high_action.setEnabled(True)
        self.auto_action.setEnabled(True)
        self.dynpm_action.setEnabled(True)

    def activate_auto(self):
        """Activate auto profile
        """
        if not power_method_set("profile", self.cards, home=HOME, client=SOCKET) or\
            not power_profile_set("auto", self.cards, home=HOME, client=SOCKET):
            self.showMessage("Error",
                NOPERM, self.Critical, 10000)
            return
        self.setIcon(QtGui.QIcon(AUTOPATH))
        self.low_action.setEnabled(True)
        self.mid_action.setEnabled(True)
        self.high_action.setEnabled(True)
        self.auto_action.setEnabled(False)
        self.dynpm_action.setEnabled(True)

    def activate_dynpm(self):
        """Activate dynpm method with default profile
        """
        if not power_profile_set("default", self.cards, home=HOME, client=SOCKET) or\
            not power_method_set("dynpm", self.cards, home=HOME, client=SOCKET):
            self.showMessage("Error",
                NOPERM, self.Critical, 10000)
            return
        self.setIcon(QtGui.QIcon(DYNPMPATH))
        self.low_action.setEnabled(True)
        self.mid_action.setEnabled(True)
        self.high_action.setEnabled(True)
        self.auto_action.setEnabled(True)
        self.dynpm_action.setEnabled(False)

    def check_status(self):
        if self.profile == "low":
            self.low_action.setEnabled(False)
            self.setIcon(QtGui.QIcon(LOWPATH))
        if self.profile == "mid":
            self.mid_action.setEnabled(False)
            self.setIcon(QtGui.QIcon(MIDPATH))
        if self.profile == "high":
            self.high_action.setEnabled(False)
            self.setIcon(QtGui.QIcon(HIGHPATH))
        if self.profile == "auto":
            self.auto_action.setEnabled(False)
            self.setIcon(QtGui.QIcon(AUTOPATH))
        if self.method == "dynpm":
            self.dynpm_action.setEnabled(False)
            self.setIcon(QtGui.QIcon(DYNPMPATH))


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
            string = radeon_info_get(client=SOCKET)
            if MAJVER == 2:
                self.showMessage("Radeon-INFO",
                    QtCore.QString.fromUtf8(string, len(string)), self.Information, 10000)
            elif MAJVER == 3:
                self.showMessage("Radeon-INFO", string, self.Information, 10000)

def main():
    """Main function
    """
    cards = verifier()
    init_method, init_profile = power_status_get(client=SOCKET).split(",")
    l_method, l_profile = last_power_status_get(HOME).split(",")
    
    # Check if is lost the last configuration
    if l_method != init_method or l_profile != init_profile:
        power_profile_set(l_profile, cards, home=HOME, client=SOCKET)
        power_method_set(l_method, cards, home=HOME, client=SOCKET)

    init_method, init_profile = power_status_get(client=SOCKET).split(",")

    if init_method == "dynpm":
        icon = DYNPMPATH
    else:
        icon = DEFAULTPATH

    app = QtGui.QApplication(sys.argv)

    wid = QtGui.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon(icon), \
        wid,
        init_method,
        init_profile,
        cards)

    tray_icon.show()
    sys.exit(app.exec_())

def client_main(client=False):
    """Client main
    """
    global SOCKET
    if client:
        CONTEXT = zmq.Context()
        SOCKET = CONTEXT.socket(zmq.REQ)
        SOCKET.connect("tcp://localhost:%s" % PORT)
    main()