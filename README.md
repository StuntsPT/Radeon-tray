#Radeon-tray

This is a small program to control the power profiles of your Radeon card via
systray icon.

It is written in PyQt4 using python 3 (also working on python 2).

It supports setups with single and multiple cards.

## Importante notice:
Not all power profiles work on all cards, and in some cases, some modes *might*
even cause crashes. This is not frequent, and in case it happens to you, you
should file a bug at freedesktop.org.

This is just to alert you that YMMV when using this program.

The program now also supports providing information regarding the card temperature if a sensor is found in a list of paths. 
Currentlly only the path for my specific card is listed, but feel free to add your own 
(and if you let me know what that path might be I will just add it here).

###Requirements:
* A radeon card (duh!) with KMS
*~~Python3~~
* Python2 or Python3 - both are supported
* PyQt4
* zmq

###Usage without installer:
Just run Radeon-tray.py. It should place an icon in your systray, which you can
right click to change the power method (dynpm or profile) and the power profile
(auto, low, mid, high or dynpm).

As normal user yuo must set the permissions of /sys/class/drm/card0/device/power_profile and of
/sys/class/drm/card0/device/power_method to be writable by your user (by
default only root can change these values and only root can read debug info);

```chmod a+w /sys/class/drm/card0/device/power_profile``` will work, but feel free to use any other method. 
To make the changes permanent don't forget to add the chmod line to your rc.local or equivalent in your distro
(If your /etc/rc.local contains an exit 0 line, then the chmod line has to be placed before it).

If you are using systemd, you can create /etc/tmpfiles.d/radeon-power-profile.conf with the following line:
```
    w /sys/class/drm/card0/device/power_profile 0666 - - - mid
    w /sys/class/drm/card0/device/power_method 0666 - - - profile
```
This will change the permissions of power_profile so that any user can change the power method and profile


Do not forget to do the same to /sys/class/drm/card1/... if you use more than one card!

That's about it.

**Note**: if you won't change files' privileges you can simply start the program with ```sudo python Radeon-tray.py```

###Usage with installer:
The installer and uninstaller scripts need root privileges. They should only be executed like bash script from the program directory: ```sudo ./installer```

The installer create a service for the tray icon that starts with the system.

You need to add manually the tray icon program to the startup programs.

```command: radeontray client```

You can also launch the command above in a shell after login.

**Note**: installer refers and work only with *systemd*.

###Credits:
You can read more about power profiles [here](http://www.x.org/wiki/RadeonFeat\
ure#KMS_Power_Management_Options "X.org documentation on Radeon power profiles"\
).

This program was inspired by my [Gnome-shell extension](https://github.com/Stun\
tsPT/shell-extension-radeon-power-profile-manager). But this one will work on
non Gnome environments.

The icons were created by Todd-partridge (https://github.com/Gen2ly) and
somewhat modified by myself.

###License:
This software is licensed under the GPLv2.
