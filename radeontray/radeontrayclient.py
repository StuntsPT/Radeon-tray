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
    power_state_set, \
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

BATPATH = ICONPATH + "/radeon-tray-battery.svg"
BALPATH = ICONPATH + "/radeon-tray-balanced.svg"
PERFPATH = ICONPATH + "/radeon-tray-performance.svg"
NOPERM = """"You don't have the permission to write card's
settings, check the official site for information!"""

class SystemTrayIcon(QtGui.QSystemTrayIcon):
    """Tray icon program for Radeon driver with kms
    """

    def __init__(self, icon, parent, method, state, cards):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)

        self.setToolTip("Radeon-Tray")
        self.method = method
        self.state = state
        self.cards = cards

        menu = QtGui.QMenu(parent)

        self.high_action = menu.addAction(QtGui.QIcon(PERFPATH), "Performance state")
        self.high_action.triggered.connect(self.activate_high)

        self.mid_action = menu.addAction(QtGui.QIcon(BALPATH), "Balanced state")
        self.mid_action.triggered.connect(self.activate_mid)

        self.low_action = menu.addAction(QtGui.QIcon(BATPATH), "Battery state")
        self.low_action.triggered.connect(self.activate_low)

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

    def activate_performance(self):
        """Activate performance state
        """
        if not power_method_set("dpm", self.cards, home=HOME, client=SOCKET) or\
            not power_state_set("performance", self.cards, home=HOME, client=SOCKET):
            self.showMessage("Error",
                NOPERM, self.Critical, 10000)
            return
        self.setIcon(QtGui.QIcon(PERFPATH))
        self.battery_action.setEnabled(True)
        self.balanced_action.setEnabled(True)
        self.performance_action.setEnabled(False)

    def activate_balanced(self):
        """Activate balanced state
        """
        if not power_method_set("dpm", self.cards, home=HOME, client=SOCKET) or\
            not power_state_set("balanced", self.cards, home=HOME, client=SOCKET):
            self.showMessage("Error",
                NOPERM, self.Critical, 10000)
            return
        self.setIcon(QtGui.QIcon(MIDPATH))
        self.battery_action.setEnabled(True)
        self.balanced_action.setEnabled(False)
        self.performance_action.setEnabled(True)

    def activate_battery(self):
        """Activate battery state
        """
        if not power_method_set("dpm", self.cards, home=HOME, client=SOCKET) or\
            not power_state_set("battery", self.cards, home=HOME, client=SOCKET):
            self.showMessage("Error",
                NOPERM, self.Critical, 10000)
            return
        self.setIcon(QtGui.QIcon(LOWPATH))
        self.battery_action.setEnabled(False)
        self.balanced_action.setEnabled(True)
        self.performance_action.setEnabled(True)

    def check_status(self):
        if self.state == "battery":
            self.battery_action.setEnabled(False)
            self.setIcon(QtGui.QIcon(BATPATH))
        if self.state == "balanced":
            self.balanced_action.setEnabled(False)
            self.setIcon(QtGui.QIcon(BALPATH))
        if self.state == "performance":
            self.high_action.setEnabled(False)
            self.setIcon(QtGui.QIcon(PERFPATH))

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
    init_method, init_state = power_status_get(client=SOCKET).split(",")
    l_method, l_state = last_power_status_get(HOME).split(",")

    # Check if is lost the last configuration
    if l_method != init_method or l_state != init_state:
        power_state_set(l_state, cards, home=HOME, client=SOCKET)
        power_method_set(l_method, cards, home=HOME, client=SOCKET)

    init_method, init_state = power_status_get(client=SOCKET).split(",")

    icon = BALPATH

    app = QtGui.QApplication(sys.argv)

    wid = QtGui.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon(icon), \
        wid,
        init_method,
        init_state,
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