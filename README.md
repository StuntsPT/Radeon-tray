#Radeon-tray

This is a small program to control the power profiles of your Radeon card via
systray icon.

It is written in PyQt4 using python 3.

It supports setups with single and multiple cards.

## Importante notice:
Not all power profiles work on all cards, and in some cases, some modes *might*
even cause crashes. This is not frequent, and in case it happens to you, you
should file a bug at freedesktop.org.

This is just to alert you that YMMV when using this program.

###Requirements:
* A radeon card (duh!);
* Python3;
* PyQt4;

###Usage:
Just run Radeon-tray.py. It should place an icon in your systray, which you can
right click to change the power method (dynpm or profile) and the power profile
(auto, low, mid or high).

That's about it.

###Credits:
You can read more about power profiles [here](http://www.x.org/wiki/RadeonFeat\
ure#KMS_Power_Management_Options "X.org documentation on Radeon power profiles")
.

This program was inspired by my [Gnome-shell extension](https://github.com/Stun\
tsPT/shell-extension-radeon-power-profile-manager). But this one will work on
non Gnome environments.