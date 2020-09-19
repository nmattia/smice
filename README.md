# SMICE

The Smart MICE. Oh, That's Smice!

This is a project for [HackZurich 2020](https://hackzurich.com/). This is a
daemon that moves the cursor between monitors, depending on where the user is
looking. This is achievd  by processing the camera feed.

## Building

Enter the nix-shell or make sure you have the following system packages installed:

* xorg (libSM, libXrender, libXext, libX11)
* libstdc++
* glib
* cmake

Follow the installation instructions for [GazeTracking](https://github.com/antoinelame/GazeTracking)
Follow the installation instructions for [pyautogui](https://pyautogui.readthedocs.io/en/latest/)

You're all set! Run `python init.py`. See lines `11` and `15` of that file for
runtime options.
