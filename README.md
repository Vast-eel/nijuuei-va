# nijuuei-va
Voice patch and rudimentary asset extraction tools for the PC version of 二重影.

Partially based on [gscScriptCompAndDecompiler](https://github.com/TesterTesterov/gscScriptCompAndDecompiler).

## Installing
### Voice patch
Save files from an unmodified version of the game may or may not crash depending on when you saved, so starting from the beginning is recommended.

Download [this](https://drive.google.com/drive/folders/1MMvA8k8tal3h6U4hwnW04e3lv066tYhq?usp=sharing) and put the Vox folder in the Nijuuei root folder.

Download script files from the Releases section and overwrite the files in the game's Ksd directory with the new files.

### QoL fixes
The game tends to crash or hang after animations on modern machines. To fix this, set the game to fullscreen (even if you want to play it windowed) then download [DxWnd](https://sourceforge.net/projects/dxwnd/) and [these](https://drive.google.com/drive/folders/1Nr5Qn2ZDqtreLOAUDnoEWtd0spksYvSF?usp=sharing) files.

Put the .exe file in the game's root folder and import the .dxw file in DxWnd.

Right click the preset, press Modify and change the path to the nocd .exe file where your game install is.

Go into the CDAudio tab and select the "Rip CD Audio" option and run the game once. After that, set it to "Use audio files". This way the game will use .wav files DxWnd puts in the root folder without needing to have the second disc inserted at all times.

Due to running the game in fullscreen and forcibly windowing it with DxWnd, the right click menu will be misaligned with your mouse cursor. If this bothers you, disable the options that force windowing in the preset's properties and change the screen mode to windowed in-game. This will make the game go fullscreen for animations, though.

## Editing
I've included the scripts written for the purposes of this patch. ksd_tool and kpd_tool are for the main scripts and Nijyuei.kpd, while dc_tool has two functions for getting voiced lines from the Dreamcast version's .BIN files and matching them with ksd_tool's decompiled scripts respectively. See the repo's wiki for technical details.

I've applied most of the Dreamcast version's script fixes to the PC version's files. The revised scripts are under Ksd\Decompiled\DC_Fixes. They're used as the base for the voice patch, the scripts of which you can see under Ksd\Voiced.

## Linux troubleshooting
If you're running Nijuuei through DxWnd, make sure to disable the "Emulate Win9X heap" option in the Libs tab of the preset to prevent crashes.

Other than that, it should run perfectly fine through Wine if you have Japanese fonts and locale properly set up (see [this](https://learnjapanese.moe/vn-linux/) guide). I last tested it on 9.4 in WoW64 mode.

By default the font rendering is a bit messed up (see wiki as to why). Use the nocd exe to fix this.

As Wine has yet to implement ddraw7's WaitForVerticalBlank function, the game will run too fast for sprite transitions to properly display. You *can* force it to slow down by changing DxWnd's vsync mode to Frequency, but I wouldn't recommend it.

The in-game volume sliders don't work. If you think the music's too loud compared to the voices, go into the CDAudio tab, tick Set emulated CD volume, then go into the Sound tab and change CD volume to your liking.