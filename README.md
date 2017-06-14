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

The program now also supports providing information regarding the card temperature
*if* a sensor is found in a list of paths. Currentlly only the path for my specific
card is listed, but feel free to add your own (and if you let me know what that path
might be I will just add it here).

###Requirements:
* A radeon card (duh!) with KMS
* ~~Python3~~
* Python2 or Python3 - both are supported
* PyQt4
* zmq

###Usage with installer:
The installer and uninstaller scripts need **root privileges**.

The installer uses setup.py, and using it is quite simple:

```pythonX setup.py install```

Where "X" is the python verion you wish to use (it could be not necessary).

####You can start the program with root privileges:

``` radeontray ```

**Note**: remember to check if the system recognize radeontray executable with ```which radeontray```

####You can also install a server/client program with systemd support:

```radeontray install-server systemd```  
```radeontray install-client```

**Note**: uninstall with ```radeontray uninstall-server systemd``` and ```radeontray uninstall-client```

####You can manage your user's configuration file with:

```radeontray install-client-conf```  
```radeontray uninstall-client-conf```

**Note**: these commands **not require root privileges**

####You need to manually add the tray icon program to the startup programs in your DE.

``` command: /usr/bin/radeontray client ```

**Note**: You can also launch the command above after login or simply ``` radeontray client & ```.


###Credits:
You can read more about power profiles [here](http://www.x.org/wiki/RadeonFeat\
ure#KMS_Power_Management_Options "X.org documentation on Radeon power profiles"\
).

This program was inspired by my [Gnome-shell extension](https://github.com/StuntsPT/shell-extension-radeon-power-profile-manager). But this one will work on
non Gnome environments.

The icons were created by Todd-partridge (https://github.com/Gen2ly) and
somewhat modified by myself.

###License:
This software is licensed under the GPLv3.
